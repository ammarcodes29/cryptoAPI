from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging

from app.config import settings
from app.models import (
    CryptocurrencyResponse, 
    CryptocurrencyListResponse, 
    CryptocurrencyListItem,
    MarketOverview,
    ErrorResponse,
    Currency
)
from app.services.livecoinwatch import LiveCoinWatchService, LiveCoinWatchError
from app.utils.validators import (
    validate_crypto_symbol, 
    validate_currency, 
    validate_limit
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="A lightweight REST API for cryptocurrency data using LiveCoinWatch",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize service
lcw_service = LiveCoinWatchService()

@app.exception_handler(LiveCoinWatchError)
async def livecoinwatch_exception_handler(request, exc: LiveCoinWatchError):
    """Handle LiveCoinWatch API errors"""
    logger.error(f"LiveCoinWatch error: {str(exc)}")
    
    if "not found" in str(exc).lower():
        status_code = 404
    elif "unauthorized" in str(exc).lower():
        status_code = 401
    elif "rate limit" in str(exc).lower():
        status_code = 429
    else:
        status_code = 502
    
    return JSONResponse(
        status_code=status_code,
        content={"error": "API Error", "message": str(exc), "status_code": status_code}
    )

@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc: ValueError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=400,
        content={"error": "Validation Error", "message": str(exc), "status_code": 400}
    )

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Cryptocurrency API is running",
        "version": settings.api_version,
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_version": settings.api_version,
        "cache_size": "N/A"  # You could implement cache size tracking
    }

@app.get(
    "/crypto/{symbol}",
    response_model=CryptocurrencyResponse,
    tags=["Cryptocurrency"],
    summary="Get cryptocurrency data",
    description="Fetch live data for a specific cryptocurrency by symbol"
)
async def get_cryptocurrency(
    symbol: str = Path(..., description="Cryptocurrency symbol (e.g., BTC, ETH)", example="BTC"),
    currency: Currency = Query(Currency.USD, description="Fiat currency for price conversion")
):
    """Get live data for a specific cryptocurrency"""
    try:
        # Validate and normalize symbol
        validated_symbol = validate_crypto_symbol(symbol)
        validated_currency = validate_currency(currency.value)
        
        # Fetch data from LiveCoinWatch
        data = await lcw_service.get_single_coin(validated_symbol, validated_currency)
        
        # Transform data to match our response model
        response_data = {
            "symbol": data.get("symbol", validated_symbol),
            "name": data.get("name", ""),
            "price": data.get("rate", 0.0),
            "change_24h": ((data.get("delta", {}).get("day", 1.0) - 1.0) * 100),
            "volume": data.get("volume", 0.0),
            "cap": data.get("cap"),
            "rank": data.get("rank")
        }
        
        return CryptocurrencyResponse(**response_data)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get(
    "/crypto",
    response_model=CryptocurrencyListResponse, 
    tags=["Cryptocurrency"],
    summary="Get multiple cryptocurrencies",
    description="Fetch data for multiple cryptocurrencies with pagination"
)
async def get_cryptocurrencies(
    limit: int = Query(20, ge=1, le=100, description="Number of cryptocurrencies to return"),
    offset: int = Query(0, ge=0, description="Number of cryptocurrencies to skip"),
    currency: Currency = Query(Currency.USD, description="Fiat currency for price conversion")
):
    """Get list of cryptocurrencies with pagination"""
    try:
        validated_limit = validate_limit(limit)
        validated_currency = validate_currency(currency.value)
        
        # Fetch data from LiveCoinWatch
        data = await lcw_service.get_coins_list(validated_currency, validated_limit, offset)
        
        # Transform data
        crypto_items = []
        for item in data:
            crypto_item = CryptocurrencyListItem(
                symbol=item.get("code", ""),
                name=item.get("name", ""),
                price=item.get("rate", 0.0),
                percent_change_24h=((item.get("delta", {}).get("day", 1.0) - 1.0) * 100),
                rank=item.get("rank")
            )
            crypto_items.append(crypto_item)
        
        return CryptocurrencyListResponse(
            data=crypto_items,
            total_count=len(crypto_items),
            currency=validated_currency
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get(
    "/search",
    response_model=CryptocurrencyListResponse,
    tags=["Search"],
    summary="Search cryptocurrencies",
    description="Search for cryptocurrencies by name or symbol"
)
async def search_cryptocurrencies(
    query: str = Query(..., min_length=1, description="Search query (name or symbol)", example="bitcoin"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    currency: Currency = Query(Currency.USD, description="Fiat currency for price conversion")
):
    """Search for cryptocurrencies by name or symbol"""
    try:
        validated_limit = validate_limit(limit, max_limit=50)
        validated_currency = validate_currency(currency.value)
        
        # Search using the service
        data = await lcw_service.search_coins(query, validated_currency, validated_limit)
        
        # Transform data
        crypto_items = []
        for item in data:
            crypto_item = CryptocurrencyListItem(
                symbol=item.get("code", ""),
                name=item.get("name", ""),
                price=item.get("rate", 0.0),
                percent_change_24h=((item.get("delta", {}).get("day", 1.0) - 1.0) * 100),
                rank=item.get("rank")
            )
            crypto_items.append(crypto_item)
        
        return CryptocurrencyListResponse(
            data=crypto_items,
            total_count=len(crypto_items),
            currency=validated_currency
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get(
    "/market/overview",
    response_model=MarketOverview,
    tags=["Market"],
    summary="Get market overview",
    description="Get overall cryptocurrency market statistics"
)
async def get_market_overview(
    currency: Currency = Query(Currency.USD, description="Fiat currency for values")
):
    """Get cryptocurrency market overview"""
    try:
        validated_currency = validate_currency(currency.value)
        
        # Fetch market overview
        data = await lcw_service.get_market_overview(validated_currency)
        
        return MarketOverview(
            total_market_cap=data.get("cap", 0.0),
            total_volume_24h=data.get("volume", 0.0),
            bitcoin_dominance=data.get("btcDominance"),
            active_cryptocurrencies=data.get("liquidity")
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)