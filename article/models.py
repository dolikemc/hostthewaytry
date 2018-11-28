from django.db import models

from places.models import Place
from traveller.models import User


# Create your models here.
class AbstractArticle(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)
    # technical data
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(editable=False, default=False)
    deleted = models.BooleanField(editable=False, default=False)

    class Meta:
        abstract = True


class TextArticle(AbstractArticle):
    text = models.TextField()
    place = models.ForeignKey(to=Place, on_delete=models.CASCADE)


class ImageArticle(AbstractArticle):
    text = models.TextField(null=True, blank=True)
    # location data
    picture = models.ImageField(help_text='Picture of your place', upload_to='', blank=True)
    longitude = models.FloatField(help_text='Where is your place (longitude)?', null=True, blank=True)
    latitude = models.FloatField(help_text='Where is your place (latitude)?', null=True, blank=True)
    copyright = models.TextField()
