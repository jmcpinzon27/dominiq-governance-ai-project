"""Command models for axis operations."""
from typing import Optional, List
from pydantic import BaseModel, Field


class AxisBase(BaseModel):
    """Base axis attributes."""
    axis_name: str = Field(..., min_length=1, max_length=100)


class CreateAxis(AxisBase):
    """Command to create a new axis."""
    pass


class UpdateAxis(BaseModel):
    """Command to update an existing axis."""
    axis_id: int
    axis_name: Optional[str] = Field(None, min_length=1, max_length=100)


class DeleteAxis(BaseModel):
    """Command to delete an axis."""
    axis_id: int


class GetAxis(BaseModel):
    """Command to get an axis by ID."""
    axis_id: int


class AxisResponse(BaseModel):
    """Response model for axis data."""
    axis_id: int
    axis_name: str

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListAxes(BaseModel):
    """Response model for listing axes."""
    axes: List[AxisResponse]
