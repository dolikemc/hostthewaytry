from django.db import models
from django.db.models import Model

from traveller.models import User


class Ground(Model):
    deleted = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    currency = models.CharField(help_text='Currency ISO 3 Code', default='EUR', max_length=3)
    country = models.CharField(max_length=2, help_text='Country Code', blank=True)
    description = models.TextField(max_length=1024, default='', blank=True,
                                   help_text='What else would you like to tell your guests?')
    name = models.CharField(max_length=200, help_text='Name of your place', null=False)

    class Meta:
        abstract = True


class TextArticle(Ground):
    text = models.TextField()


class ImageArticle(Ground):
    text = models.TextField(null=True, blank=True)
    # location data
    picture = models.ImageField(help_text='Picture of your place', upload_to='%Y/%m/%d/')
    longitude = models.FloatField(help_text='Where is your place (longitude)?', null=True, blank=True)
    latitude = models.FloatField(help_text='Where is your place (latitude)?', null=True, blank=True)
    copyright = models.TextField()

    def save(self, force_insert: bool = False, force_update: bool = False, using=None, update_fields=None):
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)
