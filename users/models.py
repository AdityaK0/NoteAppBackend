from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255)  

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Change the related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Change the related_name
        blank=True
    )

    def __str__(self):
        return self.username