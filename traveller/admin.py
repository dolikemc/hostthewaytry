from django.contrib import admin

from .models import Traveller, PlaceAccount, User

# Register your models here.
admin.site.register(Traveller)
admin.site.register(PlaceAccount)
admin.site.register(User)
