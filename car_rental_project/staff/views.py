from datetime import datetime
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import  View
from django.views.generic import ListView
from django.shortcuts import redirect
from django.db.models import Q

from rental.models import Booking, CarImage

from staff.forms import AddListingForm, AddImageForm
# Create your views here.


@method_decorator(login_required, name="dispatch")
class StaffView(ListView):
    model = Booking
    template_name = "staff_view.html"
    context_object_name = "bookings_list"
    
    def get_queryset(self):
        bookings = Booking.objects.filter(
        Q(start_date__gt=datetime.now())
        )
        bookings = bookings.order_by('start_date')
        # Get all the bookings to be manipulated by staff
        return bookings


@method_decorator(login_required, name="dispatch")
class AddListingView(View):
    template_name = "staff_add_listing.html"

    def get(self, request):
        listing_form = AddListingForm()
        image_form = AddImageForm()
        return render(request, self.template_name, {'listing_form': listing_form, 'image_form': image_form})

    def post(self, request):
        listing_form = AddListingForm(request.POST)
        image_form = AddImageForm(request.POST, request.FILES)

        if listing_form.is_valid() and image_form.is_valid():
            new_listing = listing_form.save(commit=False)
            new_listing.save()

            # Now associate the image with the new listing
            image = image_form.save(commit=False)
            image.car = new_listing
            image.save()

            return redirect('rental:car_info', pk=new_listing.pk)

        return render(request, self.template_name, {'listing_form': listing_form, 'image_form': image_form})