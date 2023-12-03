from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def future_date_validator(value):
    if value <= timezone.now().date():
        raise ValidationError("The date must be in the future")
    
def end_date_validator(start_date, end_date):
    if end_date < start_date:
        raise ValidationError("The end date must be after the start date")
    
    
# Create your models here.
class Car(models.Model):
    Gearbox1 = "Automatic"
    Gearbox2 = "Manual"

    GearboxChoices = [
        (Gearbox1, "Automatic"),
        (Gearbox2, "Manual")
    ]

    Fuel1 = "Petrol"
    Fuel2 = "Diesel"
    Fuel3 = "LPG"
    Fuel4 = "Electric"

    FuelChoices = [
        (Fuel1, "Petrol"),
        (Fuel2, "Diesel"),
        (Fuel3, "LPG"),
        (Fuel4, "Electric")
    ]

    brand = models.CharField(max_length=30, null=False)
    model = models.CharField(max_length=30, null=False)
    gearbox = models.CharField(max_length=20, choices=GearboxChoices, default="Manual")
    fuel = models.CharField(max_length=20, choices=FuelChoices, default="Diesel")
    production_year = models.PositiveIntegerField()
    color = models.CharField(max_length=30, null=False)
    daily_rate = models.IntegerField(default=30, null=False)
    
    def __str__(self) -> str:
        return f"{self.brand}, {self.model}" 


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name="car_images", on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="cars/images/")

    def __str__(self):
        return f"{self.car.brand}, {self.car.model}. {self.id}"


class Customer(models.Model):
    name = models.CharField(max_length=30, null=False)
    email = models.EmailField(null=False)
    phone_number =models.CharField(max_length=12, help_text="Please enter your phone number +2556912345678")
    ID_Number = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"{self.name}, {self.ID_Number}"
    

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    start_date = models.DateField(validators=[future_date_validator])
    end_date = models.DateField(validators=[end_date_validator])
    
    def number_of_days(self):
        return (self.end_date - self.start_date).days
    
    def total_payment(self):
        return self.car.daily_rate * self.number_of_days
    
    def __str__(self):
        return f"{self.id}, {self.car},  {self.start_date} -> {self.end_date}"
