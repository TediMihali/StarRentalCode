from django import forms
from rental.models import Car


class AddListing(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = Car
