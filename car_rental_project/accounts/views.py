from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic.edit import FormView
from .forms import SignUpForm, SignInForm
from django.urls import reverse_lazy
# Create your views here.

class SignUpView(FormView):
    template_name = "sign_up.html"
    form_class = SignUpForm
    success_url =  reverse_lazy("home")


