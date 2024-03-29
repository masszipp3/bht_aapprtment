from django import forms
from .models import Floor,Category,Room,room_status,Booking,Account,Payment,Cash_Payment,Journel,User
from datetime import date
from django.utils.dateparse import parse_datetime
from django.utils.formats import get_format


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['floor_no', 'no_of_rooms']
        widgets = {
            'floor_no': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter floor number',
                'required':True

            }),
            'no_of_rooms': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter number of rooms',
                'required':True
            }),
        }

class AddUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email','username','user_type','password']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Name',
                'required':True

            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Email',
                'required':True
            }),
             'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Username',
                'required':True

            }),
             'password': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Password',
                'required':True

            }),
              'user_type': forms.Select(attrs={
                  'class': 'form-select mb-3'
                }),
        }       

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','category_description']
        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Category Name',
                'required':True

            }),
            'category_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Description',
                'required':True
            }),

        }

  
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'floor', 'category', 'yearly_amount', 'monthly_amount', 'daily_amount', 'room_status']

        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room Number','required':True}),
            'floor': forms.Select(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example','required':True}),
            'category': forms.Select(attrs={'class': 'form-select mb-3','required':True }),
            'yearly_amount': forms.NumberInput(attrs={'class': 'form-control','required':True}),
            'monthly_amount': forms.NumberInput(attrs={'class': 'form-control','required':True}),
            'daily_amount': forms.NumberInput(attrs={'class': 'form-control','required':True}),
        }    

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'room','booking_type', 'check_in_date', 'expected_checkout_date', 'rate', 'duration', 'advance_payment','country','address','mobile','id_proof','id_no','total_amount']
        
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name', 'required': True}),
            'booking_type': forms.Select(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),
            # Similarly for other fields...
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-in Date', 'type': 'datetime-local', 'required': True}),
            'expected_checkout_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local','required': True}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'advance_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'id_proof': forms.Select(attrs={'class': 'form-select mb-3'}),
            'id_no': forms.TextInput(attrs={'class': 'form-control'}),
            # 'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control','required':True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'room': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.expected_checkout_date:
            datetime_format = get_format('DATETIME_INPUT_FORMATS')[0]  # or 'Y-m-d\TH:i' if not localized
            expected_checkout_date = self.instance.expected_checkout_date.strftime(datetime_format)
            self.initial['expected_checkout_date'] = expected_checkout_date

        if self.instance and self.instance.check_in_date:
            datetime_format = get_format('DATETIME_INPUT_FORMATS')[0]  # or 'Y-m-d\TH:i' if not localized
            check_in_date = self.instance.check_in_date.strftime(datetime_format)
            self.initial['check_in_date'] = check_in_date    


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type']
        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Name', 'required': True}),
                'account_type': forms.Select(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),
        }  


class CashReciept_form(forms.ModelForm):

    def save(self, commit=True):
        instance = super(CashReciept_form, self).save(commit=False)
        instance.payment_status = '1'
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super(CashReciept_form, self).__init__(*args, **kwargs)
        cash_account = Account.get_cash_account()
        self.fields['to_account'].initial = cash_account
        self.fields['from_account'].queryset = Account.objects.exclude(id=cash_account.id)
        # self.fields['to_account'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Payment
        fields = ['from_account', 'to_account','narration','payment_date','amount','description']
        widgets = {
                'narration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Remark', 'required': True}),
                'amount': forms.NumberInput(attrs={'class': 'form-control'}),
                'payment_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ' Date', 'type': 'date', 'required': True}),
                'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description'}),
                'from_account': forms.Select(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),
                'to_account': forms.HiddenInput(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),
        }

class CashPayment_form(forms.ModelForm):
    def save(self, commit=True):
        instance = super(CashPayment_form, self).save(commit=False)
        instance.payment_status = '1'
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super(CashPayment_form, self).__init__(*args, **kwargs)
        cash_account = Account.get_cash_account()
        self.fields['from_account'].initial = cash_account
        self.fields['to_account'].queryset = Account.objects.exclude(id=cash_account.id)
        # self.fields['to_account'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Cash_Payment
        fields = ['from_account', 'to_account','narration','payment_date','amount','description']
        widgets = {
                'narration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Remark', 'required': True}),
                'amount': forms.NumberInput(attrs={'class': 'form-control'}),
                'payment_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ' Date', 'type': 'date', 'required': True}),
                'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description'}),
                'to_account': forms.Select(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),
                'from_account': forms.HiddenInput(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),
        }  

class journal_form(forms.ModelForm):
    def save(self, commit=True):
        instance = super(journal_form, self).save(commit=False)
        instance.payment_status = '1'
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super(journal_form, self).__init__(*args, **kwargs)
        cash_account = Account.get_cash_account()  # Retrieve the cash account instance

        # Set the initial value for 'to_account' to None for the blank choice
        self.fields['to_account'].initial = None

    class Meta:
        model = Journel
        fields = ['from_account', 'to_account','narration','payment_date','amount','description']
        widgets = {
                'narration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Remark', 'required': True}),
                'amount': forms.NumberInput(attrs={'class': 'form-control'}),
                'payment_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ' Date', 'type': 'date', 'required': True}),
                'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description'}),
                'to_account': forms.Select(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),
                'from_account': forms.Select(attrs={'class': 'form-select mb-3', 'aria-label': 'Default select example', 'required': True}),

        }            