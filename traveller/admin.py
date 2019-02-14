from django.contrib import admin

from traveller.models import User
from places.models import PlaceAccount

# Register your models here.
admin.site.register(PlaceAccount)
admin.site.register(User)

admin.site.site_header = "HOST THE WAY"
admin.site.site_title = "Host The Way"
admin.site.index_title = ""
