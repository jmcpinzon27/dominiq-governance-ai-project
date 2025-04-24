import json
import os
from typing import Optional

from pydantic_settings import BaseSettings

class AWSSettings(BaseSettings):
    """AWS configuration settings."""
    STAGE: str = "dev"
    SECRET_NAME: str = ""
    BUCKET_NAME: str = "buckets"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"