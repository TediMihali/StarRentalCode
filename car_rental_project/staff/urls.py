from django.urls import path
from .views import AddListingView, StaffView

urlpatterns = [
    path('', StaffView.as_view(), name="staff_view"),
    path('add_listing/', AddListingView.as_view(),name="staff_add_listing")
]