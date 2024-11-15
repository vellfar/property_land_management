from django.db import models
from users.models import User
from properties.models import LandProperty

# Create your models here.
class Audit(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='audits', null=True)
    land_property = models.ForeignKey(LandProperty, on_delete=models.SET_NULL, related_name='audits', null=True)
    action = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.action} - {self.user.username}"