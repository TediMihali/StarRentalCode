from django.contrib import admin
from .models import Car, Booking, Customer, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1  # Number of empty forms to show for adding new images

class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'production_year', 'fuel', 'gearbox', 'color', 'daily_rate']
    search_fields = ['brand', 'model']
    inlines = [CarImageInline]  # Include CarImageInline in the CarAdmin form

    


admin.site.register(Car, CarAdmin)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(CarImage)