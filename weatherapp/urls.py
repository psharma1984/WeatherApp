from django.urls import path
from .views import LocationDetailView, RegistrationView, HomeView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("weather/", LocationDetailView.as_view(), name="weather_page"),
    path("register/", RegistrationView.as_view(), name="register"),
]
