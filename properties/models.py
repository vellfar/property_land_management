from django.db import models
from users.models import User

class LandProperty(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('under_transfer', 'Under Transfer'),
    ]
    
    property_id = models.CharField(max_length=10, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    location = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    valuation = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.property_id} - {self.location}"


class OwnershipTransfer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    
    transfer_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(LandProperty, on_delete=models.CASCADE, related_name='transfers')
    current_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_transfers')
    new_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer {self.transfer_id} - {self.status}"
