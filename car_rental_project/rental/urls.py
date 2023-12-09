from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import Home, AutoListingView, AboutUsView, CarRentView,  BookingsView, CancelBookingView, RentSuccess




urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("cars/", AutoListingView.as_view(), name="auto_listing"),
    path("cars/rent/<int:car_id>", CarRentView.as_view(), name="car_rent"),
    path("cars/rent/success", RentSuccess.as_view(), name="rent_success"),
    path("about/", AboutUsView.as_view(), name="about_us"),
    path('bookings', BookingsView.as_view(), name="bookings"),
    path('bookings/cancel/<int:booking_id>',CancelBookingView.as_view() ,name="cancel_booking"),

]
