from django.contrib import admin
from .models import Car, Booking, Customer, CarImage
from django.contrib import admin
from .models import QuickLink
from django import forms 


class CarAdminForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['images']

        
class CarAdmin(admin.ModelAdmin):
    form = CarAdminForm
    list_display = ['brand', 'model', 'production_year', 'fuel', 'gearbox', 'color', 'daily_rate']
    search_fields = ['brand', 'model']

    # If you want to customize the inline as well
    class CarImageInline(admin.TabularInline):
        model = CarImage
        extra = 1  # Number of empty forms to show for adding new images

    inlines = [CarImageInline]  # Include CarImageInline in the CarAdmin form


admin.site.register(Car, CarAdmin)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(CarImage)
admin.site.register(QuickLink)