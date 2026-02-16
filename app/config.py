"""Configuration management for CodeReview AI.

This module handles all application configuration using environment variables
with sensible defaults. Supports multiple environments (dev, staging, prod).
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator, Field
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support.
    
    All settings can be overridden via environment variables.
    For example, API_KEY can be set via the API_KEY environment variable.
    """
    
    # Application settings
    APP_NAME: str = "CodeReview AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENV")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # API Configuration
    API_KEY: Optional[str] = Field(default=None, env="API_KEY")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # GitHub Integration
    GITHUB_TOKEN: Optional[str] = Field(default=None, env="GITHUB_TOKEN")
    GITHUB_API_URL: str = "https://api.github.com"
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=4, env="WORKERS")
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Model Configuration
    DEFAULT_MODEL: str = Field(default="gpt-4", env="DEFAULT_MODEL")
    MAX_TOKENS: int = Field(default=2000, env="MAX_TOKENS")
    TEMPERATURE: float = Field(default=0.3, env="TEMPERATURE")
    
    # Code Analysis Settings
    MAX_FILE_SIZE_MB: int = Field(default=5, env="MAX_FILE_SIZE_MB")
    MAX_FILES_PER_REVIEW: int = Field(default=50, env="MAX_FILES_PER_REVIEW")
    SUPPORTED_LANGUAGES: List[str] = Field(
        default=["python", "javascript", "typescript", "java", "go", "rust", "cpp", "csharp"],
        env="SUPPORTED_LANGUAGES"
    )
    
    # Caching
    ENABLE_CACHE: bool = Field(default=True, env="ENABLE_CACHE")
    CACHE_TTL_SECONDS: int = Field(default=3600, env="CACHE_TTL_SECONDS")
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database (optional)
    DATABASE_URL: Optional[str] = Field(default=None, env="DATABASE_URL")
    
    @validator('ENVIRONMENT')
    def validate_environment(cls, v):
        """Validate environment is one of the allowed values."""
        allowed = ['development', 'staging', 'production']
        if v.lower() not in allowed:
            raise ValueError(f"Environment must be one of: {', '.join(allowed)}")
        return v.lower()
    
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        """Validate log level is supported by Python logging."""
        allowed = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of: {', '.join(allowed)}")
        return v.upper()
    
    @validator('TEMPERATURE')
    def validate_temperature(cls, v):
        """Ensure temperature is within valid range."""
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == 'production'
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == 'development'
    
    def get_api_key(self, provider: str = 'openai') -> Optional[str]:
        """Get API key for specified provider.
        
        Args:
            provider: API provider name (openai, anthropic)
            
        Returns:
            API key if available, None otherwise
        """
        if provider.lower() == 'openai':
            return self.OPENAI_API_KEY or self.API_KEY
        elif provider.lower() == 'anthropic':
            return self.ANTHROPIC_API_KEY
        return None
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.
    
    This function is cached to avoid reading environment variables
    multiple times during application lifecycle.
    
    Returns:
        Settings instance with current configuration
    """
    return Settings()


# Global settings instance
settings = get_settings()


# Environment-specific logging
if settings.is_development:
    import logging
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT
    )
