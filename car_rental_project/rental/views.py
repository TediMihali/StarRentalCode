from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from .forms import CarSearchForm, CarRentForm
from .models import Car, CarImage, Booking


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


class CarRentView(FormView):
    template_name = "rent.html"
    form_class = CarRentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_number = self.kwargs["car_id"]
        car_model = self.get_car_model(car_number)
        context["car"] = car_model
        return context
    
    def get_car_model(self, car_number):
        try:
            car_model = Car.objects.get(id=car_number)
            return car_model
        except Car.DoesNotExist:
            return None

    def form_valid(self, form):
        # Get the car model
        car_number = self.kwargs["car_id"]
        car_model = self.get_car_model(car_number)

        # Create a new Booking instance
        booking = Booking(
            car=car_model,
            start_date=form.cleaned_data["start_date"],
            end_date=form.cleaned_data["end_date"]
            # Add other fields as needed
        )

        # Save the new booking to the database
        booking.save()

        # Redirect to a success page or any other desired URL
        return redirect('home')  # Replace 'success_page' with the actual URL name for the success page
    