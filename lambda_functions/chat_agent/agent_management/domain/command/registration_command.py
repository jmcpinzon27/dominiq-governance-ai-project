"""User related commands and models."""
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

class GetUser(BaseModel):
    """Command for retrieving a user."""
    user_id: int | None = None
    email: str | None = None


class RegistrationResponse(BaseModel):
    """Response model for user data."""
    email: str
    user_id: str|None = None
    responsible: str
    subdomain: str
    domain: str
    industry: str

    class Config:
        """Pydantic configuration."""
        from_attributes = True
