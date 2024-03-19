# signals.py

from decimal import Decimal
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from .models import Booking,Payment,Transaction,Account,Cash_Payment,Journel,Customer
from django.db.models import Sum


@receiver(post_save, sender=Booking)
def create_initial_payment(sender, instance, created, **kwargs):
    if created:
        instance.create_initial_payment()
        instance.amount_due = instance.total_amount - instance.advance_payment
        instance.save()
        try:
           customer = Customer.objects.get(mobile=instance.mobile)
           customer.address = instance.address
           customer.customer_name = instance.customer_name
           customer.country = instance.country
           customer.id_proof = instance.id_proof
           customer.id_no = instance.id_no
           customer.save()
        except Customer.DoesNotExist:
            Customer.objects.create(customer_name=instance.customer_name,mobile=instance.mobile,address=instance.address,
                                    country=instance.country,id_proof=instance.id_proof,id_no=instance.id_no)   

        

@receiver(post_save, sender=Payment)
def create_transaction_for_payment(sender, instance, created, **kwargs):
    def update_or_create_transaction(account, transaction_type,description=None, narration=None,amount=None):
        transaction_date = instance.payment_date or (instance.booking.check_in_date if instance.booking else None)
        descriptions = description or get_payment_description(instance) 
        Transaction.objects.create(
            account=account,
            **{
                'date': transaction_date,
                'transaction_type': transaction_type,
                'amount': amount or instance.amount,
                'transaction_remark': narration or instance.narration,
                'description': descriptions,
                'booking': instance.booking,
                'payment': instance
            }
        )

    def get_payment_description(payment):
        if payment.booking and Payment.objects.filter(booking=payment.booking).count() > 1:
            return payment.description
        return "Advance Payment" if payment.booking else payment.description

    if created:
        if instance.to_account:
            update_or_create_transaction(instance.to_account, 'debit')
        if instance.from_account:
            update_or_create_transaction(instance.from_account, 'credit')
        amount =  Decimal(instance.amount) * Decimal(0.09)
        sgst_description = f"SGST for {instance.narration}"
        csgt_description = f"CGST for {instance.narration}"

        update_or_create_transaction(Account.get_cgst(),'credit',amount=amount,narration=csgt_description)    
        update_or_create_transaction(Account.get_sgst(),'credit',amount=amount,narration=sgst_description)    
    else:
        if instance.to_account or instance.from_account:
            transactions = Transaction.objects.filter(payment=instance)
            for transaction in transactions:
                transaction.amount = instance.amount
                transaction.date = instance.payment_date or (instance.booking.check_in_date if instance.booking else None)
                transaction.transaction_remark = instance.narration
                transaction.save()
@receiver(post_save, sender=Cash_Payment)
def create_transaction_for_cashpayment(sender, instance, created, **kwargs):

    def get_description():
        if not instance.booking:
            return instance.description

    def create_or_update_transaction(account, transaction_type):
        if not account:
            return

        date = instance.payment_date
        description = get_description()

        defaults = {
            'account': account,
            'date': date,
            'transaction_type': transaction_type,
            'amount': instance.amount,
            'transaction_remark': instance.narration,
            'description': description,
            'booking': instance.booking or None,
            'cash_payment': instance
        }

        if created:
            Transaction.objects.create(**defaults)
        else:
            Transaction.objects.filter(cash_payment=instance,transaction_type= transaction_type).update(
                account=account,
                amount=instance.amount,
                transaction_remark=instance.narration
            )
    create_or_update_transaction(instance.to_account, 'debit')
    create_or_update_transaction(instance.from_account, 'credit') 

@receiver(post_save, sender=Journel)
def create_transaction_for_journal(sender, instance, created, **kwargs):

    def get_description():
        if not instance.booking:
            return instance.description

    def create_or_update_transaction(account, transaction_type):
        if not account:
            return

        transaction_date = instance.payment_date or (instance.booking.check_in_date if instance.booking else None)
        description_text = get_description()
        description = f"{description_text} for booking {instance.booking.id}" if instance.booking else description_text

        defaults = {
            'account': account,
            'date': transaction_date,
            'transaction_type': transaction_type,
            'amount': instance.amount,
            'transaction_remark': instance.narration,
            'description': description,
            'booking': instance.booking,
            'journal': instance
        }

        if created:
            Transaction.objects.create(**defaults)
        else:
            Transaction.objects.filter(journal=instance,transaction_type= transaction_type).update(
                 account=account,
                amount=instance.amount,
                transaction_remark=instance.narration
            )

    # Handle transactions for to_account and from_account
    create_or_update_transaction(instance.to_account, 'debit')
    create_or_update_transaction(instance.from_account, 'credit')
            

@receiver(post_delete, sender=Booking)
def update_balance_on_transaction_pre_save(sender, instance, **kwargs):
    # If the transaction is being updated, we need to negate the old amount
        transactions = Transaction.objects.filter(booking=instance) 
        for transaction in transactions:
            account =Account.objects.get(id=transaction.account.id)
            total_credits = Transaction.objects.filter(account=account, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
            total_debits = Transaction.objects.filter(account=account, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
            account.balance =  total_debits - total_credits
            account.save()