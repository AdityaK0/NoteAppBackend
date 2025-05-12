from django.core.cache import cache

def clear_user_notes_cache(user_id):
    key = f"notes-{user_id}"
    cache.delete(key)
    print(f"[CACHE] Cleared notes cache for user {key}")
