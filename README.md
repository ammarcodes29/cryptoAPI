# 🪙 CryptoAPI API

A lightweight, production-ready REST API built with FastAPI that provides real-time cryptocurrency data from LiveCoinWatch. Features intelligent caching, comprehensive error handling, and bonus search capabilities.

## 🚀 Features

### Core Features
- **Single Cryptocurrency Lookup** - Get detailed data for any cryptocurrency by symbol/name
- **Multiple Cryptocurrency Data** - Fetch data for multiple coins in a single request
- **Real-time Data** - Live prices, volume, market cap, and percentage changes
- **Smart Caching** - Reduces API calls and improves response times
- **Input Validation** - Robust validation for all inputs with clear error messages

### Bonus Features
- **🔍 Cryptocurrency Search** - Find cryptocurrencies by partial name matching
- **📊 Market Overview** - Get top cryptocurrencies by market cap with filtering options

### Technical Features
- **Async/Await** - High-performance asynchronous request handling
- **Error Handling** - Comprehensive error handling with meaningful HTTP status codes
- **Rate Limiting** - Built-in protection against API abuse
- **Health Checks** - Monitoring endpoints for deployment
- **Docker Support** - Container-ready with docker-compose setup

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **HTTP Client**: httpx (async)
- **Data Validation**: Pydantic v2
- **Testing**: pytest + pytest-asyncio
- **External API**: LiveCoinWatch API
- **Cache**: In-memory with TTL

## 📁 Project Structure

```
crypto-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and routes
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── livecoinwatch.py # LiveCoinWatch API client
│   └── utils/
│       ├── __init__.py
│       ├── cache.py         # Caching utilities
│       └── validators.py    # Input validation
├── tests/
│   ├── __init__.py
│   ├── test_main.py         # API endpoint tests
│   └── test_services.py     # Service layer tests
├── requirements.txt
├── Makefile
├── .env.example
└── README.md
```

## 🚦 Quick Start

### Prerequisites
- Python 3.11+
- LiveCoinWatch API key (free at [livecoinwatch.com](https://livecoinwatch.com))

### 1. Clone and Setup
```bash
git clone <repository-url>
cd crypto-api

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your LiveCoinWatch API key
LCW_API_KEY=your_api_key_here
```

### 3. Run the API
```bash
# Using Python directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using the Makefile
make run
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## 🔌 API Endpoints

### Core Endpoints

#### 1. Get Single Cryptocurrency
```http
GET /crypto/{symbol}
```

**Parameters:**
- `symbol` (path): Cryptocurrency symbol (e.g., "BTC", "ETH") or name (e.g., "bitcoin")
- `currency` (query, optional): Fiat currency for prices (default: "USD")

**Example:**
```bash
curl "http://localhost:8000/crypto/BTC"
curl "http://localhost:8000/crypto/bitcoin?currency=EUR"
```

**Response:**
```json
{
  "name": "Bitcoin",
  "symbol": "BTC",
  "current_price": 45000.50,
  "market_cap": 850000000000,
  "volume_24h": 25000000000,
  "price_change_24h": -2.5,
  "price_change_7d": 5.8,
  "price_change_30d": 15.3,
  "last_updated": "2024-01-15T10:30:00Z",
  "currency": "USD"
}
```

#### 2. Get Multiple Cryptocurrencies
```http
GET /crypto/multiple
```

**Parameters:**
- `symbols` (query): Comma-separated list of symbols (e.g., "BTC,ETH,ADA")
- `currency` (query, optional): Fiat currency (default: "USD")

**Example:**
```bash
curl "http://localhost:8000/crypto/multiple?symbols=BTC,ETH,ADA"
```

**Response:**
```json
{
  "data": [
    {
      "name": "Bitcoin",
      "symbol": "BTC",
      "current_price": 45000.50,
      "market_cap": 850000000000,
      "volume_24h": 25000000000,
      "price_change_24h": -2.5
    },
    {
      "name": "Ethereum",
      "symbol": "ETH",
      "current_price": 3200.75,
      "market_cap": 380000000000,
      "volume_24h": 15000000000,
      "price_change_24h": 1.8
    }
  ],
  "count": 2,
  "currency": "USD"
}
```

### Bonus Endpoints

#### 3. Search Cryptocurrencies
```http
GET /search
```

**Parameters:**
- `query` (query): Search term (partial name matching)
- `limit` (query, optional): Maximum results (default: 10, max: 50)

**Example:**
```bash
curl "http://localhost:8000/search?query=bitcoin&limit=5"
```

#### 4. Market Overview
```http
GET /overview
```

**Parameters:**
- `limit` (query, optional): Number of top coins (default: 10, max: 100)
- `currency` (query, optional): Fiat currency (default: "USD")

**Example:**
```bash
curl "http://localhost:8000/overview?limit=20&currency=EUR"
```

### Utility Endpoints

#### Health Check
```http
GET /health
```

#### Root/Info
```http
GET /
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test file
pytest tests/test_main.py -v
```

### Example Test Commands
```bash
# Test single endpoint
curl "http://localhost:8000/crypto/BTC"

# Test multiple endpoints
curl "http://localhost:8000/crypto/multiple?symbols=BTC,ETH"

# Test search
curl "http://localhost:8000/search?query=bitcoin"

# Test health
curl "http://localhost:8000/health"
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LCW_API_KEY` | LiveCoinWatch API key | Required |
| `LCW_BASE_URL` | LiveCoinWatch API URL | `https://api.livecoinwatch.com` |
| `CACHE_TTL_SECONDS` | Cache time-to-live | `300` |
| `API_TITLE` | API title | `Cryptocurrency API` |
| `DEBUG` | Debug mode | `false` |

### Supported Currencies
- USD (default), EUR, GBP, JPY, CAD, AUD

## 🔒 Security & Best Practices

- ✅ Input validation and sanitization
- ✅ Rate limiting protection
- ✅ Error handling without sensitive data exposure
- ✅ Non-root Docker user
- ✅ Health checks for monitoring
- ✅ Async operations for better performance
- ✅ Proper HTTP status codes
- ✅ API key security (environment variables)

## 📊 Performance Features

- **Caching**: 5-minute TTL to reduce API calls
- **Async**: Non-blocking I/O operations
- **Connection Pooling**: Efficient HTTP client management
- **Request Batching**: Multiple coins in single request

## 🚀 What I'd Build Next

Given more time, I would add:

### Infrastructure & Scaling
- **Redis Integration** - Replace in-memory cache with Redis for production deployments
- **Database Layer** - PostgreSQL for historical data storage and analytics
- **Message Queue** - Celery/RQ for background price updates and notifications

### Advanced Features
- **WebSocket Support** - Real-time price streaming
- **Historical Data** - Price charts and historical analysis endpoints
- **Price Alerts** - User-configurable price notifications
- **Portfolio Tracking** - User accounts and portfolio management
- **Technical Indicators** - RSI, MACD, moving averages

### Monitoring & Observability
- **Metrics Collection** - Prometheus integration
- **Logging** - Structured logging with ELK stack
- **Monitoring Dashboard** - Grafana dashboards
- **Error Tracking** - Sentry integration
- **Performance Monitoring** - APM tools

### Security & Compliance
- **API Authentication** - JWT tokens and API keys
- **Rate Limiting** - Redis-based distributed rate limiting
- **CORS Configuration** - Proper cross-origin setup
- **Data Privacy** - GDPR compliance features

### Developer Experience
- **API Versioning** - Proper versioning strategy (/v1/, /v2/)
- **SDK Generation** - Auto-generated client libraries
- **Webhook Support** - Event-driven integrations
- **Batch Operations** - Bulk data processing endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and linting
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- **Documentation**: Check the `/docs` endpoint when running
- **Issues**: Open an issue on GitHub
- **API Key**: Get your free key at [LiveCoinWatch](https://livecoinwatch.com)
