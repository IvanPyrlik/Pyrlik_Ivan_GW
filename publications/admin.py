from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class Publication(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    list_filter = ('owner',)
