from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import LocationSearchForm
from .models import Location, APIRequestModel, UserData
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import requests
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.


class HomeView(TemplateView):
    template_name = "base.html"


class RegistrationView(FormView):
    template_name = "registration/register.html"

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")  # Redirect to the login page

        return render(request, self.template_name, {"form": form})


class LocationDetailView(LoginRequiredMixin, FormView):
    login_url = "/login/"
    template_name = "location_detail.html"
    form_class = LocationSearchForm

    def post(self, request, *args, **kwargs):
        form = LocationSearchForm(request.POST)
        context = self.get_context_data()

        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            units = form.cleaned_data["units"]
            if units == "metric":
                unit = "C"
            else:
                unit = "F"
            api_url = f"http://api.openweathermap.org/data/2.5/weather?q={keyword}&units={units}&appid=YOUR_KEY"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                exists_place = Location.objects.filter(Q(name__iexact=data["name"])).first()
                if exists_place:
                    place = exists_place
                else:
                    place, created = Location.objects.get_or_create(
                        name=data["name"],
                        country=data["sys"]["country"],
                        longitude=data["coord"]["lon"],
                        latitude=data["coord"]["lat"],
                    )
                    place.save()
                userdata, created = UserData.objects.get_or_create(user=request.user)
                userdata.locations.add(place)

                api_request, created = APIRequestModel.objects.get_or_create(
                    user=request.user,
                    location=place,
                    endpoint=api_url,
                )
                api_request.save()

                context["location_data"] = {
                    "city": keyword,
                    "whole": data,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "unit": unit,
                }
            else:
                context["error_message"] = "Failed to fetch location data."

        # Re-render the template with the form and results
        return self.render_to_response(context)
