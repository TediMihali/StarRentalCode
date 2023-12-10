from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from rental.models import Customer


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=12)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'password1', 'password2')

    def clean_ID_Number(self):
        id_number = self.cleaned_data['ID_Number']
        # Validate the uniqueness of ID_Number
        if User.objects.filter(customer__ID_Number=id_number).exists():
            raise forms.ValidationError("A user with this ID Number already exists.")
        return id_number

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")