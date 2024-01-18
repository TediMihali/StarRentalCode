from datetime import datetime
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import  View
from django.views.generic import ListView
from django.shortcuts import redirect
from django.db.models import Q

from rental.models import Booking, CarImage, Car

from staff.forms import AddListingForm
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
        return render(request, self.template_name, {'listing_form': listing_form})

    def post(self, request):
        listing_form = AddListingForm(request.POST, request.FILES)

        if listing_form.is_valid():
            new_listing = listing_form.save()
            images = request.FILES.getlist('image')
             
            for image in images:
                CarImage.objects.create(car=new_listing, image=image)
                
            return redirect('rental:auto_listing')

        return render(request, self.template_name, {'listing_form': listing_form})