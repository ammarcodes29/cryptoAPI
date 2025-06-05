from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CAD = "CAD"
    AUD = "AUD"


class CryptocurrencyResponse(BaseModel):
    """Response model for single cryptocurrency data"""
    symbol: str
    name: str
    price: float
    percent_change_24h: float = Field(alias="change_24h")
    volume_24h: float = Field(alias="volume")
    market_cap: Optional[float] = Field(default=None, alias="cap")
    rank: Optional[int] = None
    
    class Config:
        populate_by_name = True


class CryptocurrencyListItem(BaseModel):
    """Simplified model for cryptocurrency list responses"""
    symbol: str
    name: str
    price: float
    percent_change_24h: float
    rank: Optional[int] = None


class CryptocurrencyListResponse(BaseModel):
    """Response model for multiple cryptocurrencies"""
    data: List[CryptocurrencyListItem]
    total_count: int
    currency: str


class MarketOverview(BaseModel):
    """Market overview response"""
    total_market_cap: float
    total_volume_24h: float
    bitcoin_dominance: Optional[float] = None
    active_cryptocurrencies: Optional[int] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    status_code: int