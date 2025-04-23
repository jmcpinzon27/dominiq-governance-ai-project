"""Maturity Answer related commands and models."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class MaturityAnswerBase(BaseModel):
    """Base maturity answer attributes."""
    session_id: int = Field(..., gt=0)
    maturity_question_id: int = Field(..., gt=0)
    answer_text: str = Field(..., min_length=1)
    answered_at: datetime = Field(default_factory=datetime.now)


class CreateMaturityAnswer(MaturityAnswerBase):
    """Command for creating a maturity answer."""
    pass


class UpdateMaturityAnswer(MaturityAnswerBase):
    """Command for updating a maturity answer."""
    maturity_answer_id: int = Field(..., gt=0)


class DeleteMaturityAnswer(BaseModel):
    """Command for deleting a maturity answer."""
    maturity_answer_id: int = Field(..., gt=0)


class GetMaturityAnswer(BaseModel):
    """Command for retrieving a maturity answer."""
    maturity_answer_id: Optional[int] = Field(None, gt=0)
    session_id: Optional[int] = Field(None, gt=0)
    maturity_question_id: Optional[int] = Field(None, gt=0)


class MaturityAnswerResponse(MaturityAnswerBase):
    """Response model for maturity answer data."""
    maturity_answer_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListMaturityAnswers(BaseModel):
    """Response model for maturity answer list."""
    answers: List[MaturityAnswerResponse]


class AsistantResponse(BaseModel):
    text: str = Field(description="The generated text response")
    response_id: int = Field(default=0, description="Number of tokens used in the generation")
    timestamp: str = Field(default_factory=datetime.now, description="The timestamp of the response")
