"""Command models for industry operations."""
from typing import Optional, List
from pydantic import BaseModel, Field


class CreateIndustry(BaseModel):
    """Command to create a new industry."""
    industry_name: str = Field(..., min_length=1, max_length=100)

class UpdateIndustry(BaseModel):
    """Command to update an existing industry."""
    industry_id: int
    industry_name: Optional[str] = Field(None, min_length=1, max_length=100)

class DeleteIndustry(BaseModel):
    """Command to delete an industry."""
    industry_id: int


class GetIndustry(BaseModel):
    """Command to get an industry by ID."""
    industry_id: int


class IndustryResponse(BaseModel):
    """Response model for industry data."""
    industry_id: int
    industry_name: str

class ListIndustries(BaseModel):
    """Response model for listing industries."""
    industries: List[IndustryResponse]
