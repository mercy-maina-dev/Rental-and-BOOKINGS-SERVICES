# houses/admin.py

from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price',
                    'availability', 'landlord', 'created_at')
    list_filter = ('availability',)
    search_fields = ('title', 'location')
