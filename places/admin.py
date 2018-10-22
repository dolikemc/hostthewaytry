from django.contrib import admin

from .models import Place, Price, GeoName, Room

admin.site.register(Place)
admin.site.register(Price)
admin.site.register(Room)

admin.site.register(GeoName)
