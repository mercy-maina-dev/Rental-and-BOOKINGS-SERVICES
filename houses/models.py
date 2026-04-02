# houses/models.py

from django.db import models
from django.conf import settings


class House(models.Model):
    AVAILABILITY_CHOICES = (
        ('available',   'Available'),
        ('booked',      'Booked'),
        ('unavailable', 'Unavailable'),
    )

    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='houses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='houses/', blank=True, null=True)
    availability = models.CharField(
        max_length=15, choices=AVAILABILITY_CHOICES, default='available')
    bedrooms = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.location}"

    @property
    def is_available(self):
        return self.availability == 'available'
