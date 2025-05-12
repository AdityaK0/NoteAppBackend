from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Notes
from django.core.cache import cache
from .utils import clear_user_notes_cache


@receiver(post_save, sender=Notes)
def create_user_profile(sender, instance, created, **kwargs):
        clear_user_notes_cache(instance.user.id)
        print("RESETING CACHE VALUES ::::: ")
        
@receiver(post_delete, sender=Notes)
def clear_notes_cache_on_delete(sender, instance, **kwargs):
    # Called when a note is deleted
    clear_user_notes_cache(instance.user.id)
    print("CACHE CLEARED on DELETE")