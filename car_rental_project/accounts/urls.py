from django.urls import path
from .views import SignInView, SignUpView, logout_view

urlpatterns = [
    path("signin/", SignInView.as_view(), name='signin'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", logout_view, name="logout")
]
