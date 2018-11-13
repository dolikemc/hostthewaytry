from django.contrib.auth.models import User
from django.db import models


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=64, blank=True, null=True)
    zip = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    mobile = models.CharField(max_length=64, blank=True, null=True)
    deleted = models.BooleanField(default=False)


class Traveller(Participant):
    picture = models.ImageField()
    expiry_date = models.DateField(blank=True, null=True)


class PlaceAdmin(Participant):
    alt_email = models.EmailField(blank=True, null=True)


class Worker(Traveller):
    pass
