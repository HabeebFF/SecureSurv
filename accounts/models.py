from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin","Admin"),
        ("security","Security Personnel"),
        ("analyst","Analyst"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Person(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="faces/")
    encoding = models.BinaryField()
    is_wanted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ROLE_CHOICES = (
        ("admin","Admin"),
        ("security","Security Personnel"),
        ("analyst","Analyst"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Person(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="faces/")
    encoding = models.BinaryField()
    is_wanted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)