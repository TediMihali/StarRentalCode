from typing import Any
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CarSearchForm, CarRentForm
from .models import Car, CarImage, Booking, User


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


class CarRentView(CreateView):
    model = Booking
    template_name = "rent.html"
    form_class = CarRentForm
    success_url = reverse_lazy("home")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.kwargs["car_id"]
        context["car"] = get_object_or_404(Car, id=car_id)
        return context
    
    def form_valid(self, form):
        # Check if the form is valid
        if form.is_valid():
            # Get the car model
            car_id = self.kwargs["car_id"]
            car_model = get_object_or_404(Car, id=car_id)

            # Get the selected start_date and end_date
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            # Check if the car is available for the selected dates
            if not self.is_car_available(car_model, start_date, end_date):
                # Car is not available, handle accordingly (e.g., show an error message)
                return self.render_to_response(
                    self.get_context_data(form=form, error_message="Car is not available for the selected dates.")
                )

            # Create a new Booking instance
            booking = Booking(
                car=car_model,
                start_date=start_date,
                end_date=end_date
                # Add other fields as needed
            )

            # Save the new booking to the database
            booking.save()

            # Redirect to a success page or any other desired URL
            return redirect('home')  # Replace 'home' with the actual URL name for the success page

        # If the form is not valid, render the form again with errors
        return self.render_to_response(self.get_context_data(form=form))

    def is_car_available(self, car, start_date, end_date):
    
        overlapping_bookings = Booking.objects.filter(
             Q(start_date__lte=start_date, end_date__gte=start_date) | 
            Q(start_date__lte=end_date, end_date__gte=end_date) |    
            Q(start_date__gte=start_date, end_date__lte=end_date),     
            car=car
        )
           
        # If there are overlapping bookings, the car is not available
        return not overlapping_bookings.exists()
    

@method_decorator(login_required, name='dispatch')
class BookingsView(ListView):
    model = Booking
    template_name = "auto_listing.html"
    context_object_name = "bookings_list"

    def get_queryset(self):
        # Filter bookings based on the current user's ID
        return Booking.objects.filter(id_number=self.request.user)

