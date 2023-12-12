from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, SignInForm
from rental.models import Customer
from django.urls import reverse_lazy    
from django.contrib.auth import logout 
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('rental:home') 


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            try:
                # Try to create the User object
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                    # Add other user fields as needed
                )

                # Try to create the Customer object
                customer, created = Customer.objects.get_or_create(
                    user=user,
                    name=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number']
                    # Add other customer fields as needed
                )

                if not created:
                    # Customer already exists with the same ID_Number
                    messages.error(request, 'A customer with this ID Number already exists.')
                    return render(request, 'signup.html', {'form': form})

                # Rest of your code...

                return render(request, 'home.html')

            except IntegrityError:
                messages.error(request, 'An error occurred while creating the user and customer.')
                return render(request, 'sign_up.html', {'form': form})
        else:
            messages.error(request, 'Form is not valid. Please check the data you provided.')
            return render(request, 'sign_up.html', {'form': form})
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form': form})

class SignInView(LoginView):
    template_name = "sign_in.html"
    form_class = SignInForm

    def form_invalid(self, form):
        list(messages.get_messages(self.request))
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)
        
    def get_success_url(self) -> str:
        return reverse("rental:home")
    