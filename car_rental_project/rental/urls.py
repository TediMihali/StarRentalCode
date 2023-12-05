from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import Home, AutoListingView, AboutUsView, CarRentView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Home.as_view(), name="home"),
    path("cars/", AutoListingView.as_view(), name="auto_listing"),
    path("about/", AboutUsView.as_view(), name="about_us"),
    path("cars/rent/<int:car_id>", CarRentView.as_view(), name="car_rent")
]
