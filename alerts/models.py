from django.db import models
from recognition.models import DetectionEvent

# Create your models here.

class Alert(models.Model):
    event = models.ForeignKey(DetectionEvent, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)