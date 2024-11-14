from django.db import models

# Create your models here.
class Permission(models.Model):
    role = models.IntegerField() # 1 = Admin, 2 = Government Official, 3 = Landowner
    # Other permissions

    # End of Other Permissions
    status = models.IntegerField(default=1) # 0 Inactive, 1 Active
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)