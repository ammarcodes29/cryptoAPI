import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

@patch('app.services.livecoinwatch.LiveCoinWatchService.get_coin_data')
def test_get_cryptocurrency_success(mock_get_coin_data):
    """Test successful cryptocurrency data retrieval"""
    mock_data = {
        "name": "Bitcoin",
        "code": "BTC",
        "rate": 45000.50,
        "volume": 25000000000,
        "cap": 850000000000,
        "delta": {
            "hour": 1.2,
            "day": -2.5,
            "week": 5.8,
            "month": 15.3,
            "quarter": 25.1,
            "year": 120.5
        }
    }
    mock_get_coin_data.return_value = mock_data
    
    response = client.get("/crypto/BTC")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bitcoin"
    assert data["symbol"] == "BTC"
    assert data["current_price"] == 45000.50

@patch('app.services.livecoinwatch.LiveCoinWatchService.get_coin_data')
def test_get_cryptocurrency_not_found(mock_get_coin_data):
    """Test cryptocurrency not found"""
    mock_get_coin_data.side_effect = Exception("Coin not found")
    
    response = client.get("/crypto/INVALID")
    assert response.status_code == 404

def test_get_cryptocurrency_invalid_symbol():
    """Test invalid cryptocurrency symbol"""
    response = client.get("/crypto/123invalid")
    assert response.status_code == 422

@patch('app.services.livecoinwatch.LiveCoinWatchService.get_coins_data')
def test_get_multiple_cryptocurrencies(mock_get_coins_data):
    """Test multiple cryptocurrency data retrieval"""
    mock_data = [
        {
            "name": "Bitcoin",
            "code": "BTC",
            "rate": 45000.50,
            "volume": 25000000000,
            "cap": 850000000000,
            "delta": {"day": -2.5}
        },
        {
            "name": "Ethereum",
            "code": "ETH",
            "rate": 3200.75,
            "volume": 15000000000,
            "cap": 380000000000,
            "delta": {"day": 1.8}
        }
    ]
    mock_get_coins_data.return_value = mock_data
    
    response = client.get("/crypto/multiple?symbols=BTC,ETH")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["data"][0]["symbol"] == "BTC"
    assert data["data"][1]["symbol"] == "ETH"