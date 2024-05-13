from django.urls import path
from .views import SignInView, signup_view, logout_view, ResetPasswordView, CustomPasswordResetConfirmView, activate_account
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signin/", SignInView.as_view(), name='signin'),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/<uidb64>/set-password/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),

]

