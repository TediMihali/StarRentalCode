from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


def future_date_validator(value):
    if value <= timezone.now().date():
        raise ValidationError("The date must be in the future")


def end_date_validator(start_date, end_date):
    if end_date < start_date:
        raise ValidationError("The end date must be after the start date")


class CarSearchForm(forms.Form):
    brand = forms.CharField(max_length=30)
    location = forms.CharField(max_length=50)
    start_date = forms.DateField(validators=[future_date_validator])
    end_date = forms.DateField(validators=[end_date_validator])

# rental/forms.py




