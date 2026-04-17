from django.db import models
from accounts.models import Admin as User

# Create your models here.

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)