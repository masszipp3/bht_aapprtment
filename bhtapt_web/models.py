from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from datetime import timedelta

# Create your models here.

usertypes=(('1','Admin'),
           ('2','Appartment'),
           ('3','Staff'))

room_status=(('1','Avaialble'),
           ('2','Booked'),
           ('3','Reserved'))

booking_status=(('1','Pending'),
           ('2','Booked'),
           ('3','Completed'))

booking_type=(('1','Daily'),
           ('2','Yearly'),
           ('3','Monthly'))

payment_status=(('1','Paid'),
           ('2','Pending'),
           ('3','Rejected'))

id_proof_type=(('1','Driving Licence'),
           ('2','Passport'),
           ('3','PAN Card'))


class User(AbstractUser):
    name = models.CharField(max_length=40,null=True,blank=True)
    email = models.EmailField(unique=True, max_length=30)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(unique=True,max_length=15,null=False,blank=False)
    user_type = models.CharField(max_length=40,null=True,blank=True,choices=usertypes)
    place = models.CharField(max_length=40,null=True,blank=True)
    soft_delete = models.BooleanField(default=False,null=False)


    class Meta:
        db_table = "User"


class Floor(models.Model):
    floor_no = models.IntegerField(null=True,unique=True)
    no_of_rooms = models.IntegerField(null=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.floor_no)

class Category(models.Model):
    category_code = models.CharField(max_length=200, null=True)
    category_name = models.CharField(max_length =40,null=True,unique=True)
    category_description = models.CharField(max_length =200,null=True,)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        generated_code = "CAT-" + str(str(self.pk).zfill(5))
        self.category_code = generated_code
        super(Category, self).save(update_fields=["category_code"])

class Room(models.Model):
    room_number = models.CharField(max_length=100,null=True,blank=True,unique=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    yearly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    daily_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)   
    room_status = models.CharField(max_length=200,choices=room_status,default="1",null=True,blank=True) 

    def __str__(self):
        return self.room_number



# Add reservation status choices here or elsewhere in your code
reservation_status_choices = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed')
]
class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    reservation_status = models.CharField(max_length=100, choices=reservation_status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room.room_number} - {self.customer_name}"

    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    customer_name = models.CharField(max_length=100,null=True,blank=True)
    booking_no = models.CharField(max_length=100,null=True,blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_type = models.CharField(max_length=40,choices=booking_type)
    reservation = models.ForeignKey(Reservation,on_delete=models.SET_NULL,null=True,related_name='reservation_booking')
    check_in_date = models.DateTimeField()
    expected_checkout_date = models.DateTimeField(null=True)
    check_out_date = models.DateTimeField(null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(null=True,default=1)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=3,default=0.000)
    total_amount = models.DecimalField(max_digits=10, decimal_places=3,default=0.000)
    mobile = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=300,null=True)
    amount_due =  models.DecimalField(max_digits=10, decimal_places=3,default=0.000)
    country = models.CharField(max_length=200,null=True,blank=True)
    id_proof = models.CharField(max_length=10,null=True,blank=True,choices=id_proof_type)
    id_no = models.CharField(max_length=10,null=True,blank=True)
    # passport = models.CharField(max_length=40 ,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True,default='2',choices=booking_status)    
    discount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    soft_delete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Booking, self).save(*args, **kwargs)
        generated_code = "BOOKING-" + str(str(self.pk).zfill(5))
        self.booking_no = generated_code
        super(Booking, self).save(update_fields=["booking_no"])



    def create_initial_payment(self):
        if self.advance_payment and self.advance_payment > 0:
        # Create an initial payment
            payment = Payment.objects.create(
                booking=self,
                amount=self.advance_payment, 
                payment_status='1',  #  '1' represents a status paid
                narration='Advance Payment',
                payment_date = self.check_in_date
            )
        if self.room:
            self.room.room_status = '2'
            self.room.save()    


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,null=True,blank=True,related_name='payment_booking')
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    payment_date = models.DateField(null=True,blank=True)
    payment_status = models.CharField(max_length=50,choices=payment_status)
    narration = models.CharField(max_length=200, null=True, blank=True)


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        # Add other account types as needed
    )

    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES,null=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"
    
    def update_balance(self):
        total_credits = Transaction.objects.filter(account=self, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_debits = Transaction.objects.filter(account=self, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        self.balance =  total_debits - total_credits
        self.save()
    
    @staticmethod
    def get_cash_account():
        return Account.objects.get_or_create(name="Cash Account", account_type="cash")[0]

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_account')
    date = models.DateField()
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    transaction_remark = models.CharField(max_length=15, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.CharField(max_length=200, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions_bpoking')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions_payment')
    
    # def __str__(self):
    #     return f"{self.get_transaction_type_display()} - {self.amount} - {self.get_category_display()} on {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.account.update_balance()

    @staticmethod
    def get_balance_for_date(date):
        total_credits = Transaction.objects.filter(
            date=date, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_debits = Transaction.objects.filter(
            date=date, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        return total_debits-total_credits 


    @staticmethod
    def get_closing_balance_until_date(date):
        total_credits = Transaction.objects.filter(
            date__lte=date, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_debits = Transaction.objects.filter(
            date__lte=date, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        return total_debits-total_credits 

    @staticmethod
    def get_opening_balance_for_date(date):
        previous_day = date - timedelta(days=1)
        return Transaction.get_closing_balance_until_date(previous_day)    