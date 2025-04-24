"""Maturity agent response related commands and models."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MaturityAgentResponseBase(BaseModel):
    """Base maturity agent response attributes."""
    agent_id: int = Field(..., gt=0)
    maturity_question_id: int = Field(..., gt=0)
    response_text: str = Field(..., min_length=1)
    response_date: datetime = Field(default_factory=datetime.now)


class CreateMaturityAgentResponse(MaturityAgentResponseBase):
    """Command for creating a maturity agent response."""
    pass


class UpdateMaturityAgentResponse(MaturityAgentResponseBase):
    """Command for updating a maturity agent response."""
    maturity_agent_response_id: int = Field(..., gt=0)


class DeleteMaturityAgentResponse(BaseModel):
    """Command for deleting a maturity agent response."""
    maturity_agent_response_id: int = Field(..., gt=0)


class GetMaturityAgentResponse(BaseModel):
    """Command for retrieving a maturity agent response."""
    maturity_agent_response_id: Optional[int] = Field(None, gt=0)
    agent_id: Optional[int] = Field(None, gt=0)
    maturity_question_id: Optional[int] = Field(None, gt=0)


class MaturityAgentResponseData(MaturityAgentResponseBase):
    """Response model for maturity agent response data."""
    maturity_agent_response_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListMaturityAgentResponses(BaseModel):
    """Response model for maturity agent response list."""
    responses: List[MaturityAgentResponseData]
