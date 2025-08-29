from django.core.cache import cache

def clear_user_notes_cache(user_id: int):
    cache_key = f"notes-{user_id}"
    try:
        cache.delete(cache_key)
        print(f"Cache cleared for {cache_key}")
    except Exception as e:
        #  just skip, don’t crash signals
        print(f"Cache clear failed (Redis down?): {e}")
