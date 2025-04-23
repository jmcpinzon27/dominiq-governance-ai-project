"""Subdomain related commands and models."""
from typing import Optional, List
from pydantic import BaseModel, Field


class SubdomainBase(BaseModel):
    """Base subdomain attributes."""
    subdomain_name: str = Field(..., min_length=1, max_length=100)
    domain_id: int = Field(..., gt=0)


class CreateSubdomain(SubdomainBase):
    """Command for creating a subdomain."""
    pass


class UpdateSubdomain(SubdomainBase):
    """Command for updating a subdomain."""
    subdomain_id: int = Field(..., gt=0)


class DeleteSubdomain(BaseModel):
    """Command for deleting a subdomain."""
    subdomain_id: int = Field(..., gt=0)


class GetSubdomain(BaseModel):
    """Command for retrieving a subdomain."""
    subdomain_id: Optional[int] = Field(None, gt=0)
    subdomain_name: Optional[str] = None
    domain_id: Optional[int] = Field(None, gt=0)


class SubdomainResponse(SubdomainBase):
    """Response model for subdomain data."""
    subdomain_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListSubdomains(BaseModel):
    """Response model for subdomain list."""
    subdomains: List[SubdomainResponse]
