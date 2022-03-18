from django.contrib import admin


# Register your models here.
from .models import DayCare


class DayCareAmid(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(DayCare)
