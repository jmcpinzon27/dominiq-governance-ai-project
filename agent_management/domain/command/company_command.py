"""Company related commands and models."""
from typing import List, Optional
from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    """Base company attributes."""
    company_name: str = Field(..., min_length=1, max_length=100)
    industry_id: Optional[int] = None


class CreateCompany(CompanyBase):
    """Command for creating a company."""
    pass


class UpdateCompany(BaseModel):
    """Command for updating a company."""
    company_id: int
    company_name: Optional[str] = Field(None, min_length=1, max_length=100)
    industry_id: Optional[int] = None


class DeleteCompany(BaseModel):
    """Command for deleting a company."""
    company_id: int


class GetCompany(BaseModel):
    """Command for retrieving a company."""
    company_id: Optional[int] = None
    company_name: Optional[str] = None


class CompanyResponse(BaseModel):
    """Response model for company data."""
    company_id: int
    company_name: str
    industry_id: Optional[int] = None


class ListCompanies(BaseModel):
    """Response model for company list."""
    companies: List[CompanyResponse]
