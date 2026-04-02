# bookings/admin.py

from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'house', 'start_date',
                    'end_date', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('tenant__username', 'house__title')
