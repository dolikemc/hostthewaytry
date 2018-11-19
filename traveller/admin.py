from django.contrib import admin

from .models import Traveller, PlaceAccount

# Register your models here.
admin.site.register(Traveller)
admin.site.register(PlaceAccount)
