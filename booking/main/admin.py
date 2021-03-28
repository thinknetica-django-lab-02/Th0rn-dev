from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from ckeditor.widgets import CKEditorWidget

from .models import Room, AccommodationFacility, AccommodationManager, Tag


class CustomFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)


@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    pass


@admin.register(AccommodationFacility)
class AdminAccommodationFacilit(admin.ModelAdmin):
    pass


@admin.register(AccommodationManager)
class AdminAccommodationManager(admin.ModelAdmin):
    pass


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    pass