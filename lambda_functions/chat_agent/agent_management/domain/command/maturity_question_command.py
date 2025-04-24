"""Maturity Question related commands and models."""

from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, field_validator

from domain.command.maturity_agent_response_command import MaturityAgentResponseData


class MaturityQuestionBase(BaseModel):
    """Base maturity question attributes."""
    question_text: str = Field(..., min_length=1, max_length=1000)
    question_type: str|None = Field(
        pattern="^(multiple_choice|free_text|rating)$",
        default=None
    )
    question_order: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    axis_id: Optional[int] = Field(None, gt=0)
    industry_id: Optional[int] = Field(None, gt=0)


class CreateMaturityQuestion(MaturityQuestionBase):
    """Command for creating a maturity question."""
    pass


class UpdateMaturityQuestion(MaturityQuestionBase):
    """Command for updating a maturity question."""
    maturity_question_id: int = Field(..., gt=0)


class DeleteMaturityQuestion(BaseModel):
    """Command for deleting a maturity question."""
    maturity_question_id: int = Field(..., gt=0)


class GetMaturityQuestion(BaseModel):
    """Command for retrieving a maturity question."""
    maturity_question_id: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None
    question_type: Optional[str] = Field(
        None, pattern="^(multiple_choice|free_text|rating)$")
    axis_id: Optional[int] = Field(None, gt=0)
    industry_id: Optional[int] = Field(None, gt=0)


class MaturityQuestionResponse(MaturityQuestionBase):
    """Response model for maturity question data."""
    maturity_question_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class MaturityQuestionWithResponse(MaturityQuestionResponse):
    """Response model for maturity question with agent responses."""
    responses: List[MaturityAgentResponseData] = Field(default_factory=list)


class ListMaturityQuestions(BaseModel):
    """Response model for maturity question list."""
    questions: List[MaturityQuestionResponse]


class ChatMessage(BaseModel):
    """Data model for chat messages"""
    role: str
    content: str

class ChatRequest(BaseModel):
    """Data model for chat requests"""
    input_text: str
    session_id: str
    axis_id: int

class ChatResponse(BaseModel):
    """Data model for chat responses"""
    messages: ChatMessage
    timestamp: str

class QuestionOption(BaseModel):
    """Data model for question options"""
    id: int
    text: str
    score: Optional[float] = None

class Question(BaseModel):
    """Data model for survey questions"""
    id: int
    text: str
    options: List[QuestionOption] = Field(default_factory=list)
    category: Optional[str] = None

class SurveyResponse(BaseModel):
    """Data model for survey responses"""
    question_id: int
    selected_option_id: Optional[int] = None
    text_response: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('selected_option_id')
    def validate_response(cls, v, values):
        """Ensure either option ID or text response is provided"""
        if v is None and not values.data.get('text_response'):
            raise ValueError("Either selected_option_id or text_response must be provided")
        return v

class SurveyState(BaseModel):
    """Data model for survey state"""
    user_id: str
    messages: List[Dict[str, str]] = Field(default_factory=list)
    questions: List[Question] = Field(default_factory=list)
    current_question_idx: int = 0
    responses: Dict[str, str] = {}
