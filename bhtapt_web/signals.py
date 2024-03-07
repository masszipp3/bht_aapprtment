# signals.py

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
    if not created:
        transactions = Transaction.objects.filter(payment=instance)
        for transaction in transactions:
            transaction.amount = instance.amount
            transaction.date = instance.payment_date or (instance.booking.check_in_date if instance.booking else None)
            transaction.transaction_remark = instance.narration
            transaction.save()
        return
    # Check if this is an additional payment
    if instance.booking:
        if Payment.objects.filter(booking=instance.booking).count() > 1:
            description = "Additional payment"
        else:
            description = "Advance Payment"
    else:
        description = instance.description  

    if instance.to_account:    
        # Create a corresponding transaction
        Transaction.objects.create(
            account=instance.to_account ,
            date=instance.payment_date or instance.booking.check_in_date,
            transaction_type='debit',  #  'debit' as it's an increase in cash
            amount=instance.amount,
            transaction_remark = instance.narration,
            description=f"{description} for booking {instance.booking.id}" if instance.booking else description,
            booking=instance.booking or None,
            payment=instance,
        )


    if instance.from_account:
        Transaction.objects.create(
            account=instance.from_account ,
            date=instance.payment_date or instance.booking.check_in_date,
            transaction_type='credit' , #  'credit' as it's an decrease in cash
            amount=instance.amount,
            transaction_remark = instance.narration,
            description=f"{description} for booking {instance.booking.id}" if instance.booking else description,
            booking=instance.booking or None,
            payment=instance,
        )

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
            Transaction.objects.update_or_create(
                account=account,
                cash_payment=instance,
                defaults=defaults
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
            Transaction.objects.update_or_create(
                account=account,
                journal=instance,
                defaults=defaults
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