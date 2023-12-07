
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


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
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discounted_daily_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    images = models.ManyToManyField("CarImage", related_name="car_images", blank=False)
    location = models.CharField(default="StarRental", max_length=50)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.discounted_daily_rate = 0.8 * float(self.daily_rate)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.brand} - {self.model}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name="car_images", on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="cars/images/")


class Customer(models.Model):
    name = models.CharField(max_length=30, null=False)
    email = models.EmailField(null=False)
    phone_number =models.CharField(max_length=12, help_text="Please enter your phone number +2556912345678")
    ID_Number = models.CharField(max_length=20, unique=True)


class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    CUSTOMER = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def number_of_days(self):
        return (self.end_date - self.start_date).days


    def calculate_total_payment(self):
        return self.car.daily_rate * self.number_of_days()

    def save(self, *args, **kwargs):
        # Calculate and set the total_payment before saving
        self.car.save()
        self.total_payment = self.calculate_total_payment()
        super().save(*args, **kwargs)