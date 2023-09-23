from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)


class WeatherData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    weather_condition = models.CharField(max_length=10)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    locations = models.ManyToManyField(Location, related_name="users", blank=True)
    default_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_units = models.CharField(max_length=10, choices=[("metric", "Metric"), ("imperial", "Imperial")])
    receive_notifications = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username


class APIRequestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.URLField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.endpoint
