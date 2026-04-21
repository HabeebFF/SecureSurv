from django.db import models
from accounts.models import User


class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="location")
    latitude = models.FloatField()
    longitude = models.FloatField()
    tracking_enabled = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
