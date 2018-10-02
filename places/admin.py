from django.contrib import admin

from .models import Places, Prices, Towns, GeoName

admin.site.register(Places)
admin.site.register(Prices)
admin.site.register(Towns)
admin.site.register(GeoName)
