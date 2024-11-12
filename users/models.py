from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('landowner', 'Landowner'),
        ('official', 'Government Official'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"