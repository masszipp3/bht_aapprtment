# signals.py

from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from .models import Booking,Payment,Transaction,Account
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
        if Payment.objects.filter(booking=instance.booking).count() > 1:
            description = "Additional payment"
        else:
            description = "Advance Payment"

        # Create a corresponding transaction
        Transaction.objects.create(
            account=Account.get_cash_account(),
            date=instance.payment_date or instance.booking.check_in_date,
            transaction_type='debit',  #  'debit' as it's an increase in cash
            amount=instance.amount,
            transaction_remark = instance.narration,
            description=f"{description} for booking {instance.booking.id}",
            booking=instance.booking,
            payment=instance
        )


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