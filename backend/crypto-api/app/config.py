from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LiveCoinWatch API
    lcw_api_key: str
    lcw_base_url: str = "https://api.livecoinwatch.com"
    
    # Cache settings
    cache_ttl_seconds: int = 300
    
    # API settings
    api_title: str = "Cryptocurrency API"
    api_version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()