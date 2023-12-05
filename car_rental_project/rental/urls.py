from django.urls import path
from .views import Home, AutoListingView, AboutUsView


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("/cars/", AutoListingView.as_view(), name="auto_listing"),
    path("/about/", AboutUsView.as_view(), name="about_us"),

]
