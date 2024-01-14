from typing import Any
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from car_rental_project import settings
from .forms import CarSearchForm, CarRentFormLoggedIn, CarRentFormLoggedOut, CheckBookingForm
from .models import Car, CarImage, Booking, Customer
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail

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

            if is_car_available(car, start_date, end_date):
                try:
                    current_user = request.user if request.user.is_authenticated else None
                    customer = Customer.objects.get(user=current_user)

                    booking = Booking(
                        car=car,
                        CUSTOMER=customer,
                        name=customer.name,
                        phone_number=customer.phone_number,
                        start_date=start_date,
                        end_date=end_date
                        # Add other fields as needed
                    )
                    booking.total_payment = booking.calculate_total_payment() 
                except Customer.DoesNotExist:
                    customer = None
                    customer_email = form.customer_email
                    booking = Booking(
                        car=car,
                        CUSTOMER=customer,
                        name=name,
                        phone_number=phone_number,
                        start_date=start_date,
                        end_date=end_date
                        # Add other fields as needed
                    )
                    booking.total_payment = booking.calculate_total_payment() 
                
                booking.save()
                
                # Get dynamic values
                booking_id = booking.id
                car_name = str(car)  # Assuming __str__ method is defined in the Car model
                start_date_str = str(start_date)
                end_date_str = str(end_date)

                send_mail(
                    f"Booking with booking_id: {booking_id}",
                    f"""
                    Thank you for your booking
                    -------Booking Details---------
                    Booking ID: {booking_id}
                    Car: {car_name}
                    Start Date: {start_date}
                    End Date: {end_date}

                    We encourage you to save this email because you will need the booking id to access your booking and make changes.
                    """,
                    settings.EMAIL_HOST_USER,
                    [customer_email]
                    )

                # Using reverse with dynamic values
                redirect_link = reverse('rental:rent_success', kwargs={
                    'booking_id': booking_id,
                    'car': car_name,
                    'start_date': start_date_str,
                    'end_date': end_date_str,
                })

                return redirect(redirect_link)
            else:
                messages.error(request, "Car is not available for the selected dates.")
        else:
            messages.error(request, "Form submission error. Please check your input.")

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

def car_info(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {'car':car}   
    return render(request, 'car_info.html', context)


@method_decorator(login_required, name="dispatch")
class BookingsView(ListView):
    model = Booking
    template_name = "bookings.html"
    context_object_name = "bookings_list"
    
    def get_queryset(self):
        # Filter bookings based on the current user's ID
        return Booking.objects.filter(CUSTOMER__user=self.request.user)


class CancelBookingView( View):

    def post(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id=booking_id)
        # Add any additional logic for cancellation, such as updating the database
        booking.delete()
        if request.user.is_authenticated:
             return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the bookings list page
        else:
            return redirect("rental:home")


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


class CheckBookingsView(FormView):
    template_name = "check_bookings.html"
    form_class = CheckBookingForm

    def form_valid(self, form):
        booking_id = form.cleaned_data.get("booking_id")

        try:
            list(messages.get_messages(self.request))
            Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            messages.error(self.request, "Booking is not valid")
            return redirect("rental:check_bookings")

        # Redirect to the booking_info page with the correct booking_id
        return redirect('rental:booking_info', booking_id=booking_id)
        

class BookingInfoView(TemplateView):
    template_name = "booking_info.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        booking_id = self.kwargs['booking_id']
        try:
            booking = Booking.objects.get(id=booking_id)
            context['booking'] = booking
        except Booking.DoesNotExist:
            context['booking': None]

        return context
    

class FAQS(TemplateView):
    template_name="faq.html"

