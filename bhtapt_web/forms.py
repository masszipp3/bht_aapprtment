from django import forms
from .models import Floor,Category,Room,room_status,Booking
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
        fields = ['customer_name', 'room','booking_type', 'check_in_date', 'expected_checkout_date', 'rate', 'duration', 'advance_payment','country','address','mobile','id_proof','id_no','discount','total_amount']
        
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
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
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
