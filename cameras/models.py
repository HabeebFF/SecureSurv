from django.db import models

# Create your models here.


class Camera(models.Model):
    name = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    stream_url = models.URLField()
    is_active = models.BooleanField(default=True)