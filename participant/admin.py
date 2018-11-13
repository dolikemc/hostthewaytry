from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Worker


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class WorkerInline(admin.StackedInline):
    model = Worker

    def get_max_num(self, request, obj=None, **kwargs):
        return 1


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (WorkerInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
