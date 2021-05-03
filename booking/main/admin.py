from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.html import format_html

from ckeditor.widgets import CKEditorWidget

from .models import (Room, AccommodationFacility, AccommodationManager,
                    Profile, Subscriber, SMSLog)


def make_published(self, request, queryset):
    queryset.update(status='p')


def make_archived(self, request, queryset):
    queryset.update(status='a')


make_published.short_description = "Mark selected rooms as published"
make_archived.short_description = "Mark selected rooms as archived"


class CustomFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)


class AccommodationFacilityInline(admin.TabularInline):
    model = AccommodationFacility
    extra = 1


@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ("number", "hotel", "created", "status", "tags_list")
    actions = [make_published, make_archived]
    ordering = ['hotel']
    list_filter = ('tags', 'created')

    def tags_list(self, obj):
        return format_html("<br />".join([tag for tag in obj.tags]))

    tags_list.empty_value_display = "-"
    tags_list.short_description = "Теги"


@admin.register(AccommodationFacility)
class AdminAccommodationFacility(admin.ModelAdmin):
    pass


@admin.register(AccommodationManager)
class AdminAccommodationManager(admin.ModelAdmin):
    fields = (("last_name", "first_name", "middle_name"), "profile")
    list_display = ("__str__", "profile")
    inlines = [AccommodationFacilityInline]


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class AdminSubscriber(admin.ModelAdmin):
    pass


@admin.register(SMSLog)
class AdminSMSLog(admin.ModelAdmin):
    pass

