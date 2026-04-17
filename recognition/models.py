from django.db import models
from accounts.models import Person
from cameras.models import Camera

# Create your models here.


class DetectionEvent(models.Model):
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    confidence = models.FloatField()
    image = models.ImageField(upload_to="detections/")
    timestamp = models.DateTimeField(auto_now_add=True)