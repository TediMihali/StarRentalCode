from django.urls import path
from .views import SignInView, signup_view, logout_view

urlpatterns = [
    path("signin/", SignInView.as_view(), name='signin'),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout")
]
