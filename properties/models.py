from django.db import models
from users.models import User

class Document(models.Model):
    store_name = models.CharField(max_length=255) # Store name of the document
    original_name = models.CharField(max_length=255) # True Name of Document
    uploaded_date = models.DateTimeField(auto_now_add=True)
    document_type = models.CharField(max_length=255) # pdf, Image
    purpose = models.CharField(max_length=255) # Land Map, Ownership Document
    status = models.IntegerField(default=1) # 0 Deleted, 1 Active
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Location(models.Model):
    village = models.CharField(max_length=255)
    parish = models.CharField(max_length=255)
    sub_county = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    status = models.IntegerField(default=1) # 0 Deleted, 1 Active
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.village}, {self.parish}, {self.sub_county}, {self.county}, {self.district}, {self.country}"

class LandProperty(models.Model):  
    name = models.CharField(max_length=255)
    PID = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    size = models.DecimalField(max_digits=10, decimal_places=2) # Area In Acres
    valuation = models.DecimalField(max_digits=15, decimal_places=2)
    land_map = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=1) # 0 Deleted, 1 Available, 2 Under Transfer
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


class OwnershipTransfer(models.Model):
    
    property_id = models.ForeignKey(LandProperty, on_delete=models.SET_NULL, related_name='transfers', null=True)
    current_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_transfers')
    new_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers')
    request_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1) # 0 Denied, 1 Pending, 2 Approved
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_transfers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transfer {self.transfer_id} - {self.status}"
