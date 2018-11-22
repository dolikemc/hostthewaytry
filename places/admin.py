from django.contrib import admin

from places.models import Place, Price, GeoName, Room

admin.site.site_header = "HOST THE WAY"
admin.site.site_title = "Host The Way"
admin.site.index_title = ""


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    list_display = ('id', 'name', 'country', 'generated_description', 'created_on', 'deleted', 'reviewed')
    list_filter = ('deleted', 'reviewed', 'country')
    actions = ['publish', 'unpublish', 'mark_deleted', 'unmark_deleted']

    def publish(modeladmin, request, queryset):
        queryset.update(reviewed=True)

    publish.short_description = "Set the reviewed flag to true so it is published and visible in the www"

    def unpublish(modeladmin, request, queryset):
        queryset.update(reviewed=False)

    unpublish.short_description = "Set the reviewed flag to false not visible in the www"

    def mark_deleted(modeladmin, request, queryset):
        queryset.update(deleted=True)

    mark_deleted.short_description = "Soft delete means is marked as deleted but can still be reused"

    def unmark_deleted(modeladmin, request, queryset):
        queryset.update(deleted=False)

    unmark_deleted.short_description = "Soft delete means undone"


admin.site.register(Place, PlaceAdmin)
admin.site.register(Price)
admin.site.register(Room)

admin.site.register(GeoName)
