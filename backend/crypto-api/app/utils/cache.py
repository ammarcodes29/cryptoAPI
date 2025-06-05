import time
from typing import Optional, Dict, Any
from app.config import settings


class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, ttl: int = None):
        self.ttl = ttl or settings.cache_ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if time.time() - entry["timestamp"] > self.ttl:
            del self._cache[key]
            return None
        
        return entry["value"]
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp"""
        self._cache[key] = {
            "value": value,
            "timestamp": time.time()
        }
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)


# Global cache instance
cache = SimpleCache()