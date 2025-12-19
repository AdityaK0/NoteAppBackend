import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from users.models import CustomUser
from django.conf import settings

class Notes(models.Model):
    CATEGORIES = [
        ("Work", "Work"),
        ("Personal", "Personal"),
        ("Ideas", "Ideas"),
        ("Important", "Important"),
        ("Daily Work", "Daily Work"),
        ("Miscellaneous", "Miscellaneous"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES, default="Work")
    ispinned = models.BooleanField(default=False)
    
    # SaaS Power Features
    is_public = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    share_token = models.UUIDField(
    null=True,
        blank=True,
        editable=False,
    )

    
    tags = models.CharField(max_length=300,blank=True,null=False) 
    created_at = models.DateTimeField(default=now, editable=False)  
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.is_public and not self.share_token:
            self.share_token = uuid.uuid4()
        super().save(*args, **kwargs)
    
