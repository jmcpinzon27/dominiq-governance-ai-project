"""Logging configuration."""
import logging.config
import sys
from pydantic_settings import BaseSettings

class LoggingSettings(BaseSettings):
    """Logging settings."""
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"

def setup_logging():
    """Configure logging."""
    settings = LoggingSettings()
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": settings.LOG_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 1024 * 1024,  # 1MB
                "backupCount": 3,
                "formatter": "default",
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console", "file"],
        },
    }
    
    logging.config.dictConfig(logging_config)