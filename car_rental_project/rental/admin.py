from django.contrib import admin
from .models import Car, Booking, Customer


# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'production_year','fuel', 'gearbox', 'color', 'daily_rate']
    search_fields = ['brand', 'model']

admin.site.register(Car, CarAdmin)
admin.site.register(Booking);
admin.site.register(Customer);
