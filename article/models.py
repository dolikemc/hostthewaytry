from django.db import models

from places.models import Place
from traveller.models import User


# Create your models here.
class AbstractArticle(models.Model):
    place = models.ForeignKey(to=Place, on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(editable=False, default=False)
    deleted = models.BooleanField(editable=False, default=False)

    class Meta:
        abstract = True


class TextArticle(AbstractArticle):
    text = models.TextField()


class ImageArticle(AbstractArticle):
    text = models.TextField(null=True, blank=True)
    # location data
    picture = models.ImageField(help_text='Picture of your place', upload_to='%Y/%m/%d/')
    longitude = models.FloatField(help_text='Where is your place (longitude)?', null=True, blank=True)
    latitude = models.FloatField(help_text='Where is your place (latitude)?', null=True, blank=True)
    copyright = models.TextField()

    def save(self, force_insert: bool = False, force_update: bool = False, using=None, update_fields=None):
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)
