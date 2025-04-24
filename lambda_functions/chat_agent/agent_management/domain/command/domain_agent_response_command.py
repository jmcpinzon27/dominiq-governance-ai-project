"""Domain agent response related commands and models."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class DomainAgentResponseBase(BaseModel):
    """Base domain agent response attributes."""
    agent_id: int = Field(..., gt=0)
    domain_question_id: int = Field(..., gt=0)
    response_text: str = Field(..., min_length=1)
    response_date: datetime = Field(default_factory=datetime.now)


class CreateDomainAgentResponse(DomainAgentResponseBase):
    """Command for creating a domain agent response."""
    pass


class UpdateDomainAgentResponse(DomainAgentResponseBase):
    """Command for updating a domain agent response."""
    domain_agent_response_id: int = Field(..., gt=0)


class DeleteDomainAgentResponse(BaseModel):
    """Command for deleting a domain agent response."""
    domain_agent_response_id: int = Field(..., gt=0)


class GetDomainAgentResponse(BaseModel):
    """Command for retrieving a domain agent response."""
    domain_agent_response_id: Optional[int] = Field(None, gt=0)
    agent_id: Optional[int] = Field(None, gt=0)
    domain_question_id: Optional[int] = Field(None, gt=0)


class DomainAgentResponseData(DomainAgentResponseBase):
    """Response model for domain agent response data."""
    domain_agent_response_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListDomainAgentResponses(BaseModel):
    """Response model for domain agent response list."""
    responses: List[DomainAgentResponseData]
