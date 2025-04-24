"""Role related commands and models."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """Base role attributes."""
    role_name: str
    # description: str|None = None


class CreateRole(RoleBase):
    """Command for creating a role."""
    pass


class UpdateRole(RoleBase):
    """Command for updating a role."""
    role_id: int


class DeleteRole(BaseModel):
    """Command for deleting a role."""
    role_id: int


class GetRole(BaseModel):
    """Command for retrieving a role."""
    role_id: int | None = None
    role_name: int | None = None


class RoleResponse(RoleBase):
    """Response model for role data."""
    role_id: int
    # created_at: datetime
    # updated_at:datetime|None = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListRoles(BaseModel):
    """Response model for role list."""
    roles: List[RoleResponse]
