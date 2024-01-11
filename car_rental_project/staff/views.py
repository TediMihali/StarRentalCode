from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import  View
from django.views.generic import ListView
from django.shortcuts import redirect

from rental.models import Booking

from staff.forms import AddListing
# Create your views here.


@method_decorator(login_required, name="dispatch")
class StaffView(ListView):
    model = Booking
    template_name = "staff_view.html"
    context_object_name = "bookings_list"
    
    def get_queryset(self):
        # Get all the bookings to be manipulated by staff
        return Booking.objects.all()


@method_decorator(login_required, name="dispatch")
class AddListingView(View):
    def get(self, request):
        form = AddListing()
        return render(request, 'staff_add_listing.html', {'form': form})

    def post(self, request):
        form = AddListing(request.POST)
        if form.is_valid():
            new_listing = form.save()
            return redirect('rental:car_info', pk=new_listing.pk)
        return render(request, 'staff_add_listing.html', {'form': form})