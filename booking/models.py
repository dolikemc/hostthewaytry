from django.db import models

from places.models import Place, Room
from traveller.models import User


# Create your models here.
class Booking(models.Model):
    place = models.OneToOneField(to=Place, on_delete=models.CASCADE)
    traveller = models.OneToOneField(to=User, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    kids = models.PositiveIntegerField(default=0)
    message = models.TextField(blank=True, null=True)
    room = models.ForeignKey(to=Room, null=True, on_delete=models.CASCADE)
    # technical data
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: {self.traveller.display_name}@{self.place}'
