import httpx
from typing import Dict, Any, List, Optional
from app.config import settings
from app.utils.cache import cache
import logging

logger = logging.getLogger(__name__)


class LiveCoinWatchError(Exception):
    """Custom exception for LiveCoinWatch API errors"""
    pass


class LiveCoinWatchService:
    """Service for interacting with LiveCoinWatch API"""
    
    def __init__(self):
        self.base_url = settings.lcw_base_url
        self.api_key = settings.lcw_api_key
        self.headers = {
            "content-type": "application/json",
            "x-api-key": self.api_key
        }
    
    async def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to LiveCoinWatch API"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=data,
                    headers=self.headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise LiveCoinWatchError("Invalid API key or unauthorized access")
                elif response.status_code == 404:
                    raise LiveCoinWatchError("Endpoint not found")
                elif response.status_code == 429:
                    raise LiveCoinWatchError("Rate limit exceeded")
                else:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get("error", {}).get("description", "Unknown error")
                    raise LiveCoinWatchError(f"API error ({response.status_code}): {error_msg}")
                    
        except httpx.TimeoutException:
            raise LiveCoinWatchError("Request timeout - API may be unavailable")
        except httpx.RequestError as e:
            raise LiveCoinWatchError(f"Network error: {str(e)}")
    
    async def get_single_coin(self, symbol: str, currency: str = "USD") -> Dict[str, Any]:
        """Get data for a single cryptocurrency"""
        cache_key = f"coin_{symbol}_{currency}"
        
        # Check cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for {symbol}")
            return cached_data
        
        # Make API request
        data = {
            "currency": currency,
            "code": symbol,
            "meta": True
        }
        
        try:
            result = await self._make_request("coins/single", data)
            
            # Cache the result
            cache.set(cache_key, result)
            logger.info(f"Fetched and cached data for {symbol}")
            
            return result
            
        except LiveCoinWatchError as e:
            if "not found" in str(e).lower():
                raise LiveCoinWatchError(f"Cryptocurrency '{symbol}' not found")
            raise
    
    async def get_coins_list(self, currency: str = "USD", limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get list of cryptocurrencies"""
        cache_key = f"coins_list_{currency}_{limit}_{offset}"
        
        # Check cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for coins list")
            return cached_data
        
        # Make API request
        data = {
            "currency": currency,
            "sort": "rank",
            "order": "ascending",
            "offset": offset,
            "limit": limit,
            "meta": False
        }
        
        result = await self._make_request("coins/list", data)
        
        # Cache the result
        cache.set(cache_key, result)
        logger.info(f"Fetched and cached coins list")
        
        return result
    
    async def search_coins(self, query: str, currency: str = "USD", limit: int = 10) -> List[Dict[str, Any]]:
        """Search for cryptocurrencies by name or symbol"""
        cache_key = f"search_{query}_{currency}_{limit}"
        
        # Check cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Get a larger list and filter locally (since LiveCoinWatch doesn't have a search endpoint)
        coins_data = await self.get_coins_list(currency=currency, limit=200)
        
        query_lower = query.lower()
        matching_coins = []
        
        for coin in coins_data:
            if (query_lower in coin.get("name", "").lower() or 
                query_lower in coin.get("code", "").lower()):
                matching_coins.append(coin)
                
                if len(matching_coins) >= limit:
                    break
        
        # Cache the result
        cache.set(cache_key, matching_coins)
        
        return matching_coins
    
    async def get_market_overview(self, currency: str = "USD") -> Dict[str, Any]:
        """Get market overview data"""
        cache_key = f"market_overview_{currency}"
        
        # Check cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Make API request to overview endpoint
        data = {"currency": currency}
        
        result = await self._make_request("overview", data)
        
        # Cache the result
        cache.set(cache_key, result)
        
        return result