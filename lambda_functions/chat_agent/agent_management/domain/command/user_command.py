"""User related commands and models."""
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Base user attributes."""
    user_name: str
    email: str
    role_id: int
    company_id: int


class CreateUser(UserBase):
    """Command for creating a user."""
    pass


class UpdateUser(UserBase):
    """Command for updating a user."""
    user_id: int


class DeleteUser(BaseModel):
    """Command for deleting a user."""
    user_id: int


class GetUser(BaseModel):
    """Command for retrieving a user."""
    user_id: int | None = None
    email: str | None = None


class UserResponse(UserBase):
    """Response model for user data."""
    user_id: int
    # created_at: datetime
    # updated_at: datetime | None = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListUsers(BaseModel):
    """Response model for user list."""
    users: List[UserResponse]
