from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, SignInForm
from django.urls import reverse_lazy    
from django.contrib.auth import logout
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('home') 

class SignUpView(CreateView):
    template_name = "sign_up.html"
    form_class = SignUpForm
    
    def get_success_url(self) -> str:

        return reverse("rental:home")
    
    

class SignInView(LoginView):
    template_name = "sign_in.html"
    form_class = SignInForm

    def get_success_url(self) -> str:
        return reverse("rental:home")
    