from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking


# def future_date_validator(value):
#     if value <= timezone.now().date():
#         raise ValidationError("The date must be in the future")


# def end_date_validator(start_date, end_date):
#     if end_date < start_date:
#         raise ValidationError("The end date must be after the start date")


class CarSearchForm(forms.Form):
    brand = forms.CharField(max_length=30)
    location = forms.CharField(max_length=50)

    start_date = forms.DateField()
    end_date = forms.DateField()


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
        
# class CarRentFormLoggedOut(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['first_name', 'last_name', 'id_number', 'phone_number, 'start_date', 'end_date']
    
    
