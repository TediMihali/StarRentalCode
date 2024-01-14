from django import forms
from rental.models import Car, CarImage


class AddListingForm(forms.ModelForm):
    image = forms.ImageField(label='Images', required=False)

    class Meta:
        model = Car
        fields = ['brand', 'model', 'gearbox', 'fuel', 'production_year', 'color', 'daily_rate', 'discounted_daily_rate', 'location']