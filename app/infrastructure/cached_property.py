from cachetools import TTLCache
from app.core.config import settings


def cached_property(func):
    """Decorator to cache instance property values."""

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_cache'):
            self._cache = TTLCache(maxsize=settings.MAX_SIZE_CACHE, ttl=settings.TTL_CACHE)
        key = (func.__name__, args, frozenset(kwargs.items()))
        if key not in self._cache:
            self._cache[key] = func(self, *args, **kwargs)
        return self._cache[key]
    return wrapper
