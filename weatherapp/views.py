from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import LocationSearchForm
from .models import Location, WeatherData, APIRequestModel
import requests

# Create your views here.


class LocationDetailView(FormView):
    template_name = "location_detail.html"
    form_class = LocationSearchForm

    def post(self, request, *args, **kwargs):
        form = LocationSearchForm(request.POST)
        context = self.get_context_data()

        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            api_url = f"http://api.openweathermap.org/data/2.5/weather?q={keyword}&units=metric&appid=636c5b8925e9a426ca99941d04857fc6"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                location, created = Location.objects.get_or_create(
                    name=data["name"],
                    country=data["sys"]["country"],
                    longitude=data["coord"]["lon"],
                    latitude=data["coord"]["lat"],
                )
                context["location_data"] = {
                    "city": keyword,
                    "whole": data,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                }
            else:
                context["error_message"] = "Failed to fetch location data."

        # Re-render the template with the form and results
        return self.render_to_response(context)
