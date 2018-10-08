from django.contrib import admin

from .models import Place, Price, GeoName

admin.site.register(Place)
admin.site.register(Price)

admin.site.register(GeoName)
