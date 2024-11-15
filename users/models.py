from django.contrib.auth.models import AbstractUser
from django.db import models
# from properties.models import LandProperty

class User(AbstractUser):
    role = models.IntegerField(default=3)  # 1 = Admin, 2 = Government Official, 3 = Landowner
    nin = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

    def details(self):
        # properties = []
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "properties": [property for property in self.properties.filter(status=1).values()],
        }
