from typing import Any
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CarSearchForm, CarRentFormLoggedIn, CarRentFormLoggedOut
from .models import Car, CarImage, Booking
from django.shortcuts import render
from django.contrib import messages
from .models import QuickLink




class Home(TemplateView):
    template_name = "home.html"
    extra_context = {"cars": Car.objects.all(), "images": CarImage.objects.all()}


class SearchView(FormView):
    template_name = "car_search.html"
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

# views.py
def car_rent_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = CarRentFormLoggedIn(request.POST) if request.user.is_authenticated else CarRentFormLoggedOut(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get("name", "")
            phone_number = form.cleaned_data.get('phone_number')
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")

            if not is_car_available(car, start_date, end_date):
                messages.error(request, "The car is not available for the selected dates.")
                return render(request, 'rent.html', {'form': form, 'car': car})

            booking = Booking(
                car=car,
                name=name,
                phone_number=phone_number,
                start_date=start_date,
                end_date=end_date
                # Add other fields as needed
            )

            booking.save()

            # Get dynamic values
            booking_id = booking.id
            car_name = str(car)  # Assuming __str__ method is defined in the Car model
            start_date_str = str(start_date)
            end_date_str = str(end_date)

            # Using reverse with dynamic values
            redirect_link = reverse('rental:rent_success', kwargs={
                'booking_id': booking_id,
                'car': car_name,
                'start_date': start_date_str,
                'end_date': end_date_str,
            })

            return redirect(redirect_link)

    else:
        form = CarRentFormLoggedIn() if request.user.is_authenticated else CarRentFormLoggedOut()

    return render(request, 'rent.html', {'form': form, 'car': car})

def is_car_available(car, start_date, end_date):
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

    def your_view(request):
        quick_links = QuickLink.objects.all()
        return render(request, 'base.html', {'quick_links': quick_links})

    def home(request):
        return render(request, 'home.html')

def rent_success(request, booking_id, car, start_date, end_date):
    booking = get_object_or_404(Booking, id=booking_id)

    context = {
        'booking': booking,
        'car': car,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'rent_success.html', context)
