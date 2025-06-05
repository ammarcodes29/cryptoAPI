import re
from typing import List


def validate_crypto_symbol(symbol: str) -> str:
    """
    Validate and normalize cryptocurrency symbol
    Returns uppercase symbol if valid, raises ValueError if invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    # Remove whitespace and convert to uppercase
    symbol = symbol.strip().upper()
    
    # Check if symbol contains only letters and numbers
    if not re.match(r'^[A-Z0-9]+$', symbol):
        raise ValueError("Symbol must contain only letters and numbers")
    
    # Check length (most crypto symbols are 2-10 characters)
    if len(symbol) < 1 or len(symbol) > 10:
        raise ValueError("Symbol must be between 1 and 10 characters")
    
    return symbol


def validate_currency(currency: str) -> str:
    """
    Validate fiat currency code
    Returns uppercase currency if valid
    """
    if not currency or not isinstance(currency, str):
        raise ValueError("Currency must be a non-empty string")
    
    currency = currency.strip().upper()
    
    # List of supported currencies (based on common fiat currencies)
    supported_currencies = {
        'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'KRW', 'INR'
    }
    
    if currency not in supported_currencies:
        raise ValueError(f"Currency '{currency}' not supported. Supported: {', '.join(supported_currencies)}")
    
    return currency


def validate_limit(limit: int, max_limit: int = 100) -> int:
    """
    Validate limit parameter for list endpoints
    """
    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer")
    
    if limit < 1:
        raise ValueError("Limit must be at least 1")
    
    if limit > max_limit:
        raise ValueError(f"Limit cannot exceed {max_limit}")
    
    return limit


def validate_crypto_symbols(symbols: List[str]) -> List[str]:
    """
    Validate and normalize a list of cryptocurrency symbols
    """
    if not symbols or not isinstance(symbols, list):
        raise ValueError("Symbols must be a non-empty list")
    
    if len(symbols) > 50:  # Reasonable limit for batch requests
        raise ValueError("Cannot request more than 50 symbols at once")
    
    validated_symbols = []
    for symbol in symbols:
        try:
            validated_symbols.append(validate_crypto_symbol(symbol))
        except ValueError as e:
            raise ValueError(f"Invalid symbol '{symbol}': {str(e)}")
    
    return validated_symbols