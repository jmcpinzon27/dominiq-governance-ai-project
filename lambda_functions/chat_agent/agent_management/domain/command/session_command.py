"""Session related commands and models."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    """Base session attributes."""
    user_id: int = Field(..., gt=0)
    session_token: str = Field(..., min_length=32, max_length=256)
    is_active: bool = Field(default=True)
    session_start: datetime = Field(default_factory=datetime.now)
    session_end: Optional[datetime] = None


class CreateSession(SessionBase):
    """Command for creating a session."""
    pass


class UpdateSession(SessionBase):
    """Command for updating a session."""
    session_id: int = Field(..., gt=0)


class DeleteSession(BaseModel):
    """Command for deleting a session."""
    session_id: int = Field(..., gt=0)


class GetSession(BaseModel):
    """Command for retrieving a session."""
    session_id: Optional[int] = Field(None, gt=0)
    session_token: Optional[str] = None
    user_id: Optional[int] = None


class SessionResponse(SessionBase):
    """Response model for session data."""
    session_id: int
    created_at: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListSessions(BaseModel):
    """Response model for session list."""
    sessions: List[SessionResponse]
