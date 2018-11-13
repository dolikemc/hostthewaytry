from django.contrib.auth.models import User
from django.db import models


class Traveller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField()
    phone = models.CharField(max_length=64)
