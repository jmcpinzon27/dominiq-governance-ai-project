"""Agent related commands and models."""
from typing import Optional, List
from pydantic import BaseModel, Field


class AgentBase(BaseModel):
    """Base agent attributes."""
    agent_name: str = Field(..., min_length=1, max_length=100)
    agent_role: Optional[str] = Field(None, max_length=200)
    agent_type: Optional[str] = Field(None, max_length=50)


class CreateAgent(AgentBase):
    """Command for creating an agent."""
    pass


class UpdateAgent(AgentBase):
    """Command for updating an agent."""
    agent_id: int = Field(..., gt=0)


class DeleteAgent(BaseModel):
    """Command for deleting an agent."""
    agent_id: int = Field(..., gt=0)


class GetAgent(BaseModel):
    """Command for retrieving an agent."""
    agent_id: Optional[int] = Field(None, gt=0)
    agent_name: Optional[str] = None
    agent_type: Optional[str] = None


class AgentResponse(AgentBase):
    """Response model for agent data."""
    agent_id: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ListAgents(BaseModel):
    """Response model for agent list."""
    agents: List[AgentResponse]
