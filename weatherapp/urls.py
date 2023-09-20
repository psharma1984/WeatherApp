from django.urls import path
from .views import LocationDetailView

urlpatterns = [
    path("weatherapp/", LocationDetailView.as_view()),
]
