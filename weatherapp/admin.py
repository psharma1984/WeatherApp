from django.contrib import admin
from .models import Location, WeatherData, APIRequestModel, UserData

# Register your models here.
admin.site.register(Location)
admin.site.register(WeatherData)
admin.site.register(APIRequestModel)
admin.site.register(UserData)
