import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from app.services.livecoinwatch import LiveCoinWatchService, LiveCoinWatchError

@pytest.fixture
def service():
    return LiveCoinWatchService()

@pytest.mark.asyncio
@patch('httpx.AsyncClient.post')
async def test_get_coin_data_success(mock_post, service):
    """Test successful coin data retrieval"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Bitcoin",
        "code": "BTC",
        "rate": 45000.50,
        "volume": 25000000000,
        "cap": 850000000000,
        "delta": {
            "hour": 1.2,
            "day": -2.5,
            "week": 5.8
        }
    }
    mock_post.return_value = mock_response
    
    result = await service.get_coin_data("BTC")
    
    assert result["name"] == "Bitcoin"
    assert result["code"] == "BTC"
    assert result["rate"] == 45000.50
    mock_post.assert_called_once()

@pytest.mark.asyncio
@patch('httpx.AsyncClient.post')
async def test_get_coin_data_not_found(mock_post, service):
    """Test coin not found"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Coin not found"
    mock_post.return_value = mock_response
    
    with pytest.raises(LiveCoinWatchError):
        await service.get_coin_data("INVALID")

@pytest.mark.asyncio
@patch('httpx.AsyncClient.post')
async def test_get_coin_data_api_error(mock_post, service):
    """Test API error handling"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal server error"
    mock_post.return_value = mock_response
    
    with pytest.raises(LiveCoinWatchError):
        await service.get_coin_data("BTC")

@pytest.mark.asyncio
@patch('httpx.AsyncClient.post')
async def test_get_coins_data_success(mock_post, service):
    """Test successful multiple coins data retrieval"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
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
    mock_post.return_value = mock_response
    
    result = await service.get_coins_data(["BTC", "ETH"])
    
    assert len(result) == 2
    assert result[0]["code"] == "BTC"
    assert result[1]["code"] == "ETH"
    mock_post.assert_called_once()

@pytest.mark.asyncio
@patch('httpx.AsyncClient.post')
async def test_search_coins_success(mock_post, service):
    """Test successful coin search"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "name": "Bitcoin",
            "code": "BTC",
            "rate": 45000.50
        },
        {
            "name": "Bitcoin Cash",
            "code": "BCH", 
            "rate": 250.30
        }
    ]
    mock_post.return_value = mock_response
    
    result = await service.search_coins("bitcoin")
    
    assert len(result) == 2
    assert result[0]["name"] == "Bitcoin"
    assert result[1]["name"] == "Bitcoin Cash"
    mock_post.assert_called_once()