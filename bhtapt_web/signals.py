# signals.py

from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from .models import Booking,Payment,Transaction,Account,Cash_Payment,Journel
from django.db.models import Sum


@receiver(post_save, sender=Booking)
def create_initial_payment(sender, instance, created, **kwargs):
    if created:
        instance.create_initial_payment()
        instance.amount_due = instance.total_amount - instance.advance_payment
        instance.save()
        

@receiver(post_save, sender=Payment)
def create_transaction_for_payment(sender, instance, created, **kwargs):
    if created:
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
    if created:
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
                cash_payment=instance,
            )

        if instance.from_account:
            Transaction.objects.create(
                account=instance.from_account ,
                date=instance.payment_date or instance.booking.check_in_date,
                transaction_type='credit' , #  'credit' as it's an deccrease in cash
                amount=instance.amount,
                transaction_remark = instance.narration,
                description=f"{description} for booking {instance.booking.id}" if instance.booking else description,
                booking=instance.booking or None,
                cash_payment=instance,
            )  
    else:
        if instance.to_account:    
        # Create a corresponding transaction
           if transaction := Transaction.objects.filter(
                account=instance.to_account ,
                cash_payment=instance
            ).last():
               transaction.account=instance.to_account
               transaction.date=instance.payment_date
               transaction.amount = instance.amount
               transaction.transaction_remark = instance.narration
               transaction.description = instance.description
               transaction.booking=instance.booking or None
               transaction.save()

        if instance.from_account:    
        # Create a corresponding transaction
           if transaction := Transaction.objects.filter(
                account=instance.from_account ,
                cash_payment=instance
            ).last():
               transaction.account=instance.from_account
               transaction.date=instance.payment_date
               transaction.amount = instance.amount
               transaction.transaction_remark = instance.narration
               transaction.description = instance.description
               transaction.booking=instance.booking or None
               transaction.save()   

@receiver(post_save, sender=Journel)
def create_transaction_for_journal(sender, instance, created, **kwargs):
    if created:
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
                journal=instance,
            )

        if instance.from_account:
            Transaction.objects.create(
                account=instance.from_account ,
                date=instance.payment_date or instance.booking.check_in_date,
                transaction_type='credit' , #  'credit' as it's an deccrease in cash
                amount=instance.amount,
                transaction_remark = instance.narration,
                description=f"{description} for booking {instance.booking.id}" if instance.booking else description,
                booking=instance.booking or None,
                journal=instance,
            )  
    else:
        if instance.to_account:    
        # Create a corresponding transaction
           if transaction := Transaction.objects.filter(
                account=instance.to_account ,
                journal=instance
            ).last():
               transaction.account=instance.to_account
               transaction.date=instance.payment_date
               transaction.amount = instance.amount
               transaction.transaction_remark = instance.narration
               transaction.description = instance.description
               transaction.booking=instance.booking or None
               transaction.save()
        if instance.from_account:    
        # Create a corresponding transaction
           if transaction := Transaction.objects.filter(
                account=instance.from_account ,
                journal=instance
            ).last():
               transaction.account=instance.from_account
               transaction.date=instance.payment_date
               transaction.amount = instance.amount
               transaction.transaction_remark = instance.narration
               transaction.description = instance.description
               transaction.booking=instance.booking or None
               transaction.save()              

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