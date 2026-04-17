from django.db import models

# Create your models here.

class DeviceLocation(models.Model):
    device_id = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)