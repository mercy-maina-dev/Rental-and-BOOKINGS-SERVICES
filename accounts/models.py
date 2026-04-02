# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tenant',   'Tenant'),
        ('landlord', 'Landlord'),
        ('admin',    'Admin'),
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='tenant')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    # helper properties — use these in templates & views
    @property
    def is_tenant(self):
        return self.role == 'tenant'

    @property
    def is_landlord(self):
        return self.role == 'landlord'

    @property
    def is_admin_user(self):
        return self.role == 'admin'
