from django.urls import path
from .views import Home, AutoListingView, AboutUsView, car_rent_view,  BookingsView, CancelBookingView, rent_success, CheckBookingsView, BookingInfoView, FAQS, StaffView




urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("cars/", AutoListingView.as_view(), name="auto_listing"),
    path("cars/rent/<int:car_id>", car_rent_view, name="car_rent"),
    path('cars/rent/success/<int:booking_id>/<str:car>/<str:start_date>/<str:end_date>/', rent_success, name='rent_success'),
    
    path("booking/<int:booking_id>", BookingInfoView.as_view(), name="booking_info"),
    path('bookings', BookingsView.as_view(), name="bookings"),
    path('check/bookings', CheckBookingsView.as_view(), name="check_bookings"),
    path('bookings/cancel/<int:booking_id>',CancelBookingView.as_view() ,name="cancel_booking"),

    path("about/", AboutUsView.as_view(), name="about_us"),
    path("faqs", FAQS.as_view(), name='faqs'),

    path('staff/', StaffView.as_view(), name="staff_view")
]
