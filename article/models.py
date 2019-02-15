import logging

from django.db import models
from django.db.models import Model

from traveller.models import User

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class Article(Model):
    rank = models.PositiveIntegerField(default=1)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TextArticle(Article):
    text = models.TextField()


class ImageArticle(Article):
    text = models.TextField(null=True, blank=True)
    # location data
    picture = models.ImageField(help_text='Picture of your place', upload_to='%Y/%m/%d/')
    longitude = models.FloatField(help_text='Where is your place (longitude)?', null=True, blank=True)
    latitude = models.FloatField(help_text='Where is your place (latitude)?', null=True, blank=True)
    copyright = models.TextField()

    def save(self, force_insert: bool = False, force_update: bool = False, using=None, update_fields=None):
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)
