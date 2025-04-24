"""Domain related commands and models."""
from typing import Optional, List
from pydantic import BaseModel, Field


class DomainBase(BaseModel):
    """Base domain attributes."""
    domain_name: str = Field(..., min_length=1, max_length=100)


class CreateDomain(DomainBase):
    """Command for creating a domain."""
    pass


class UpdateDomain(DomainBase):
    """Command for updating a domain."""
    domain_id: int = Field(..., gt=0)


class DeleteDomain(BaseModel):
    """Command for deleting a domain."""
    domain_id: int = Field(..., gt=0)


class GetDomain(BaseModel):
    """Command for retrieving a domain."""
    domain_id: Optional[int] = Field(None, gt=0)
    domain_name: Optional[str] = None


class DomainResponse(DomainBase):
    """Response model for domain data."""
    domain_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListDomains(BaseModel):
    """Response model for domain list."""
    domains: List[DomainResponse]
