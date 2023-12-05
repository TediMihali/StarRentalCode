from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import CarSearchForm
from .models import Car, CarImage




class Home(TemplateView):
    template_name = "home.html"
    extra_context = {"cars": Car.objects.all(), "images": CarImage.objects.all()}

class SearchView(FormView):
    template = "car_search.html"
    form_class = CarSearchForm

    def form_valid(self, form):
        location = form.cleaned_data("location")
        brand = form.cleaned_data("brand")
        start_date = form.cleaned_data("start_date")
        end_date = form.cleaned_data("end_date")

class AutoListingView(ListView):
    model = Car
    template_name = "auto_listing.html"
    context_object_name = "car_list"

class AboutUsView(TemplateView):
    template_name="about_us.html"


