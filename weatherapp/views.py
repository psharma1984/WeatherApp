from django.shortcuts import render
from django.views.generic import FormView
from .forms import LocationSearchForm

# Create your views here.


class LocationDetailView(FormView):
    template_name = "location_detail.html"
    form_class = LocationSearchForm

    def post(self, request, *args, **kwargs):
        form = LocationSearchForm(request.POST)

        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            api_url = f"http://"
