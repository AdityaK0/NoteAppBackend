from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Notes
from django.core.cache import cache
from .utils import clear_user_notes_cache


@receiver(post_save, sender=Notes)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        clear_user_notes_cache(instance.user.id)
        print("RESETING CACHE VALUES ::::: ")
        
        # val = cache.get('book_data')
        # if val:
        #     cache.delete('book_data')
        #     print("CACHE VALUE RESETTED ::::: ")