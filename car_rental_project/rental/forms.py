from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking

class CarSearchForm(forms.Form):
    brand = forms.CharField(max_length=30)
    location = forms.CharField(max_length=50)

    start_date = forms.DateField()
    end_date = forms.DateField()

# forms.py
class CarRentFormLoggedIn(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']  # Add other fields as needed

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError("The end date must be after the start date")

        if end_date and end_date <= timezone.now().date():  
            raise ValidationError("The date must be in the future")
        
class CarRentFormLoggedOut(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Booking
        fields = ['name', 'phone_number', 'email', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer_email = None


    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError("The end date must be after the start date")

        if end_date and end_date <= timezone.now().date():
            raise ValidationError("The date must be in the future")\
            
        self.customer_email = cleaned_data.get('email', '')

    def save(self, commit=True):
    # Access the saved email from the customer_email attribute
        email = getattr(self, 'customer_email', '')

        # If you want to do something with the email before saving, you can do it here

        return super().save(commit)
        
class CheckBookingForm(forms.Form):
    booking_id = forms.IntegerField()

