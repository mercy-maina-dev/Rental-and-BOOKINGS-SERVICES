# bookings/models.py

from django.db import models
from django.conf import settings
from houses.models import House


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(
        blank=True, help_text="Optional message to landlord")

    def __str__(self):
        return f"{self.tenant.username} → {self.house.title} ({self.status})"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days

    @property
    def total_cost(self):
        return self.duration_days * self.house.price
