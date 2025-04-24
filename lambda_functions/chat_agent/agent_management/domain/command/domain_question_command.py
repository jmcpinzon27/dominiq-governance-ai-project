"""Domain Question related commands and models."""
from typing import Optional, List
from pydantic import BaseModel, Field


class DomainQuestionBase(BaseModel):
    """Base domain question attributes."""
    domain_id: int = Field(..., gt=0)
    industry_id: Optional[int] = Field(None, gt=0)
    question_text: str = Field(..., min_length=1, max_length=1000)
    question_type: str = Field(...,
                               pattern="^(multiple_choice|free_text|rating)$")
    category: Optional[str] = Field(None, max_length=100)


class CreateDomainQuestion(DomainQuestionBase):
    """Command for creating a domain question."""
    pass


class UpdateDomainQuestion(DomainQuestionBase):
    """Command for updating a domain question."""
    domain_question_id: int = Field(..., gt=0)


class DeleteDomainQuestion(BaseModel):
    """Command for deleting a domain question."""
    domain_question_id: int = Field(..., gt=0)


class GetDomainQuestion(BaseModel):
    """Command for retrieving a domain question."""
    domain_question_id: Optional[int] = Field(None, gt=0)
    domain_id: Optional[int] = Field(None, gt=0)
    industry_id: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None
    question_type: Optional[str] = Field(
        None, pattern="^(multiple_choice|free_text|rating)$")


class DomainQuestionResponse(DomainQuestionBase):
    """Response model for domain question data."""
    domain_question_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListDomainQuestions(BaseModel):
    """Response model for domain question list."""
    questions: List[DomainQuestionResponse]
