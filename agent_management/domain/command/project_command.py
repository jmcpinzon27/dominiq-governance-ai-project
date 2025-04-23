"""Project related commands and models."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project attributes."""
    project_name: str = Field(..., min_length=1, max_length=100)
    company_id: int = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)


class CreateProject(ProjectBase):
    """Command for creating a project."""
    pass


class UpdateProject(ProjectBase):
    """Command for updating a project."""
    project_id: int = Field(..., gt=0)


class DeleteProject(BaseModel):
    """Command for deleting a project."""
    project_id: int = Field(..., gt=0)


class GetProject(BaseModel):
    """Command for retrieving a project."""
    project_id: Optional[int] = Field(None, gt=0)
    project_name: Optional[str] = None
    company_id: Optional[int] = Field(None, gt=0)


class ProjectResponse(ProjectBase):
    """Response model for project data."""
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListProjects(BaseModel):
    """Response model for project list."""
    projects: List[ProjectResponse]
