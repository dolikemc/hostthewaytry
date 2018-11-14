from django.contrib.auth.models import User
from django.db import models


class Participant(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    street = models.CharField(max_length=64, blank=True, null=True)
    zip = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    mobile = models.CharField(max_length=64, blank=True, null=True)
    picture = models.ImageField(null=True, blank=True)
    expiry_date = models.DateField(blank=True, null=True)
    alt_email = models.EmailField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}"
