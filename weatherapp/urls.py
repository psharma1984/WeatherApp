from django.urls import path
from .views import LocationDetailView, RegistrationView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", LocationDetailView.as_view(), name="home"),
    path("register/", RegistrationView.as_view(), name="register"),
]
