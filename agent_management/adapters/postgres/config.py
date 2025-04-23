import json
import os
from dotenv import load_dotenv
from typing import Optional

import boto3
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder

load_dotenv()


class DatabaseLocalSettings(BaseSettings):
    """Local database configuration settings."""
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "agent_management"
    DB_SCHEMA: str = "public"
    USE_LOCAL_DB: bool = False
    ECHO_SQL: bool = False
    SSH_HOST: str|None= None
    SSH_PORT: int|None = None                      
    SSH_USERNAME: str|None = None
    SSH_PKEY: str|None = None

    class Config:
        """Pydantic configuration."""
        env_file = ".env",
        extra = 'allow'

class AWSSettings(BaseSettings):
    """AWS configuration settings."""
    STAGE: str = "dev"
    SECRET_NAME: str = ""

    class Config:
        """Pydantic configuration."""
        env_file = ".env"

def get_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
    """Retrieve secret from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        raise ValueError(f"Failed to retrieve secret: {str(e)}")

class DatabaseSettings(BaseSettings):
    """Database configuration settings with AWS Secrets support."""
    db_secret: Optional[dict] = None
    local_settings: DatabaseLocalSettings = DatabaseLocalSettings()
    
    @property
    def database_url(self) -> str:
        """Generate database URL from AWS Secrets or environment variables."""
        if self.local_settings.USE_LOCAL_DB:
            return (
                f"postgresql+asyncpg://"
                f"{self.local_settings.DB_USERNAME}"
                f":{self.local_settings.DB_PASSWORD}@"
                f"{self.local_settings.DB_HOST if not self.local_settings.SSH_HOST else 'localhost'}"
                f":{self.local_settings.DB_PORT}/"
                f"{self.local_settings.DB_NAME}"
            )
        
        if not self.db_secret:
            aws_settings = AWSSettings()
            self.db_secret = get_secret(
                f"{aws_settings.STAGE}/database"
            )
        
        return (
            f"postgresql+asyncpg://"
            f"{self.db_secret['username']}:{self.db_secret['password']}@"
            f"{self.db_secret['host']}:{self.db_secret['port']}/"
            f"{self.db_secret['dbname']}"
        )

def create_engine(settings: DatabaseSettings):
    """Create database engine with proper configurations."""
    return create_async_engine(
        settings.database_url,
        echo=settings.local_settings.ECHO_SQL,
        future=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )

async def get_session() -> AsyncSession:
    """Get database session."""
    settings = DatabaseSettings()

    if settings.local_settings.SSH_HOST:
        # Create SSH tunnel
        tunnel = SSHTunnelForwarder(
        (os.getenv('SSH_HOST'), int(os.getenv('SSH_PORT', 22))),
        ssh_username=os.getenv('SSH_USERNAME'),
        ssh_pkey=os.getenv('SSH_PKEY'),
        remote_bind_address=(os.getenv('DB_HOST'), int(os.getenv('DB_PORT', 5432))),
        local_bind_address=('localhost', int(os.getenv('DB_PORT', 5432)))
    )
    
    # Iniciar el túnel
    tunnel.start()

    # Update database connection to use tunnel
    engine = create_engine(settings)
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            if settings.local_settings.SSH_HOST:
                tunnel.stop()
    

metadata = MetaData(schema=DatabaseSettings().local_settings.DB_SCHEMA)
Base = declarative_base(metadata=metadata)
