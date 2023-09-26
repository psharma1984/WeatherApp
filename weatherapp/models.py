from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):  # show the actual city name on the dashboard
        return self.name

    class Meta:  # show the plural of city as cities instead of citys
        verbose_name_plural = "cities"


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
