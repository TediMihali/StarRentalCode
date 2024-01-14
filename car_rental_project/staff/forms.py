from django import forms
from rental.models import Car, CarImage


class AddListingForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'gearbox', 'fuel', 'production_year', 'color', 'daily_rate', 'discounted_daily_rate', 'location', 'available']

    avaliable = forms.BooleanField(initial=True)


class AddImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']