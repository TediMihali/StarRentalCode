from datetime import timezone
from typing import Any
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView
<<<<<<< HEAD
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CarSearchForm, CarRentForm
from .models import Car, CarImage, Booking, User
=======
from .forms import CarSearchForm
from .models import Car, CarImage


>>>>>>> 7baa5142b1a9a4ef426c5c4d0259608b0ed032bc


class Home(TemplateView):
    template_name = "home.html"
    extra_context = {"cars": Car.objects.all(), "images": CarImage.objects.all()}


class SearchView(FormView):
    template = "car_search.html"
    form_class = CarSearchForm

    def form_valid(self, form):
        location = form.cleaned_data["location"]
        brand = form.cleaned_data["brand"]
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]


class AutoListingView(ListView):
    model = Car
    template_name = "auto_listing.html"
    context_object_name = "car_list"


class AboutUsView(TemplateView):
    template_name="about_us.html"


@method_decorator(login_required, name='dispatch')
class CarRentView(FormView):
    template_name = "rent.html"
    form_class = CarRentForm


    def form_valid(self, form):
        user_instance = self.request.user
        car_id = self.kwargs["car_id"]
        car = get_object_or_404(Car, id=car_id)

        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]

        if not self.is_car_available(car, start_date, end_date):
            return self.form_invalid(form)

        booking = Booking(
            car=car,
            start_date=start_date,
            end_date=end_date,
            CUSTOMER=user_instance 
            # Add other fields as needed
        )

        booking.save()

        return redirect('rental:home')  # Replace 'home' with the actual URL name for the success page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.kwargs["car_id"]
        context["car"] = get_object_or_404(Car, id=car_id)
        return context

    def is_car_available(self, car, start_date, end_date):
        overlapping_bookings = Booking.objects.filter(
            Q(start_date__lte=start_date, end_date__gte=start_date) |
            Q(start_date__lte=end_date, end_date__gte=end_date) |
            Q(start_date__gte=start_date, end_date__lte=end_date),
            car=car
        )

        return not overlapping_bookings.exists()

@method_decorator(login_required, name="dispatch")
class BookingsView(ListView):
    model = Booking
    template_name = "bookings.html"
    context_object_name = "bookings_list"
    
    def get_queryset(self):
        # Filter bookings based on the current user's ID
        return Booking.objects.filter(
            CUSTOMER=self.request.user
            )


class CancelBookingView( View):
    def post(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id=booking_id, CUSTOMER=request.user)
        # Add any additional logic for cancellation, such as updating the database
        booking.delete()
        return redirect('rental:bookings')  # Redirect to the bookings list page
