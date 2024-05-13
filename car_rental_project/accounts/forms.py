from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from rental.models import Customer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

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
        
        
class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise ValidationError("This account is inactive.")

        return self.cleaned_data