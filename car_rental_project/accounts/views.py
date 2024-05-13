from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, SignInForm
from rental.models import Customer
from django.urls import reverse_lazy    
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView
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

                user.is_active = False
                

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

                current_site = get_current_site(request)
                subject = 'Activate Your Account'
                message = f"Hi {user.username}, please click the following link to activate your account: "
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"{current_site.domain}/activate/{uid}/{token}/"

                send_mail(subject, message + activation_link, 'from@example.com', [user.email], fail_silently=False)

                return render(request, 'pending_activation.html')
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
    

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('rental:home')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
    success_url = reverse_lazy('rental:home')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())
    
def activate_account(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=backend)
            return redirect('rental:home')  # Adjust the redirect to your 'home' URL name
        else:
            return render(request, 'activation_invalid.html')  # Ensure this template exists
    else:  
        return redirect('rental:home')
        
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('rental:home')  # Update this line to the correct home URL name
