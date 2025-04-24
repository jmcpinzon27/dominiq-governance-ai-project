"""Tests for maturity agent response operations."""
import pytest
from datetime import datetime
from httpx import AsyncClient
from fastapi import FastAPI

from domain.command.maturity_agent_response_command import (
    CreateMaturityAgentResponse,
    UpdateMaturityAgentResponse,
    GetMaturityAgentResponse,
    MaturityAgentResponseData
)
from adapters.postgres.models.maturity_agent_response import MaturityAgentResponse
from adapters.postgres.models.maturity_question import MaturityQuestion
from adapters.postgres.models.agent import Agent
from adapters.postgres.repositories.maturity_agent_response_repository import MaturityAgentResponseRepository


@pytest.mark.asyncio
async def test_create_maturity_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test creating a new maturity agent response."""
    # Create test agent and maturity question
    agent = Agent(
        agent_name="Test Agent",
        agent_role="Test Role"
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question",
        question_type="multiple_choice"
    )
    test_session.add_all([agent, maturity_question])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(maturity_question)
    
    # Arrange
    maturity_agent_response_data = {
        "agent_id": agent.agent_id,
        "maturity_question_id": maturity_question.maturity_question_id,
        "response_text": "Test response",
        "response_date": datetime.now().isoformat()
    }
    
    # Act
    response = await client.post("/maturity-agent-responses/", json=maturity_agent_response_data)
    
    # Assert
    assert response.status_code == 200
    maturity_agent_response_id = response.json()
    assert isinstance(maturity_agent_response_id, int)
    
    # Verify in database
    repository = MaturityAgentResponseRepository(test_session)
    maturity_agent_response = await repository.get(
        GetMaturityAgentResponse(maturity_agent_response_id=maturity_agent_response_id)
    )
    assert maturity_agent_response is not None
    assert maturity_agent_response.agent_id == maturity_agent_response_data["agent_id"]
    assert maturity_agent_response.maturity_question_id == maturity_agent_response_data["maturity_question_id"]
    assert maturity_agent_response.response_text == maturity_agent_response_data["response_text"]


@pytest.mark.asyncio
async def test_update_maturity_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test updating a maturity agent response."""
    # Create test agent and maturity question
    agent = Agent(
        agent_name="Test Agent for Update",
        agent_role="Test Role"
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question for update",
        question_type="multiple_choice"
    )
    test_session.add_all([agent, maturity_question])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(maturity_question)
    
    # Create a maturity agent response to update
    maturity_agent_response = MaturityAgentResponse(
        agent_id=agent.agent_id,
        maturity_question_id=maturity_question.maturity_question_id,
        response_text="Original response"
    )
    test_session.add(maturity_agent_response)
    await test_session.commit()
    await test_session.refresh(maturity_agent_response)
    
    # Arrange
    update_data = {
        "agent_id": agent.agent_id,
        "maturity_question_id": maturity_question.maturity_question_id,
        "response_text": "Updated response",
        "response_date": datetime.now().isoformat()
    }
    
    # Act
    response = await client.put(
        f"/maturity-agent-responses/{maturity_agent_response.maturity_agent_response_id}",
        json=update_data
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    repository = MaturityAgentResponseRepository(test_session)
    updated_response = await repository.get(
        GetMaturityAgentResponse(maturity_agent_response_id=maturity_agent_response.maturity_agent_response_id)
    )
    assert updated_response.response_text == update_data["response_text"]


@pytest.mark.asyncio
async def test_delete_maturity_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test deleting a maturity agent response."""
    # Create test agent and maturity question
    agent = Agent(
        agent_name="Test Agent for Delete",
        agent_role="Test Role"
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question for delete",
        question_type="multiple_choice"
    )
    test_session.add_all([agent, maturity_question])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(maturity_question)
    
    # Create a maturity agent response to delete
    maturity_agent_response = MaturityAgentResponse(
        agent_id=agent.agent_id,
        maturity_question_id=maturity_question.maturity_question_id,
        response_text="Response to delete"
    )
    test_session.add(maturity_agent_response)
    await test_session.commit()
    await test_session.refresh(maturity_agent_response)
    
    # Act
    response = await client.delete(
        f"/maturity-agent-responses/{maturity_agent_response.maturity_agent_response_id}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    repository = MaturityAgentResponseRepository(test_session)
    deleted_response = await repository.get(
        GetMaturityAgentResponse(maturity_agent_response_id=maturity_agent_response.maturity_agent_response_id)
    )
    assert deleted_response is None


@pytest.mark.asyncio
async def test_get_maturity_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test getting a maturity agent response by ID."""
    # Create test agent and maturity question
    agent = Agent(
        agent_name="Test Agent for Get",
        agent_role="Test Role"
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question for get",
        question_type="multiple_choice"
    )
    test_session.add_all([agent, maturity_question])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(maturity_question)
    
    # Create a maturity agent response to get
    maturity_agent_response = MaturityAgentResponse(
        agent_id=agent.agent_id,
        maturity_question_id=maturity_question.maturity_question_id,
        response_text="Response to get"
    )
    test_session.add(maturity_agent_response)
    await test_session.commit()
    await test_session.refresh(maturity_agent_response)
    
    # Act
    response = await client.get(
        f"/maturity-agent-responses/{maturity_agent_response.maturity_agent_response_id}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["maturity_agent_response_id"] == maturity_agent_response.maturity_agent_response_id
    assert data["agent_id"] == maturity_agent_response.agent_id
    assert data["maturity_question_id"] == maturity_agent_response.maturity_question_id
    assert data["response_text"] == maturity_agent_response.response_text


@pytest.mark.asyncio
async def test_list_maturity_agent_responses(app: FastAPI, client: AsyncClient, test_session):
    """Test listing maturity agent responses with filters."""
    # Create test agents and maturity questions
    agent1 = Agent(agent_name="Test Agent 1", agent_role="Test Role")
    agent2 = Agent(agent_name="Test Agent 2", agent_role="Test Role")
    maturity_question1 = MaturityQuestion(
        question_text="Test maturity question 1",
        question_type="multiple_choice"
    )
    maturity_question2 = MaturityQuestion(
        question_text="Test maturity question 2",
        question_type="free_text"
    )
    test_session.add_all([agent1, agent2, maturity_question1, maturity_question2])
    await test_session.commit()
    await test_session.refresh(agent1)
    await test_session.refresh(agent2)
    await test_session.refresh(maturity_question1)
    await test_session.refresh(maturity_question2)
    
    # Create maturity agent responses
    maturity_agent_responses = [
        MaturityAgentResponse(
            agent_id=agent1.agent_id,
            maturity_question_id=maturity_question1.maturity_question_id,
            response_text="Response 1"
        ),
        MaturityAgentResponse(
            agent_id=agent1.agent_id,
            maturity_question_id=maturity_question2.maturity_question_id,
            response_text="Response 2"
        ),
        MaturityAgentResponse(
            agent_id=agent2.agent_id,
            maturity_question_id=maturity_question1.maturity_question_id,
            response_text="Response 3"
        )
    ]
    for response in maturity_agent_responses:
        test_session.add(response)
    await test_session.commit()
    
    # Act - Get all responses
    response = await client.get("/maturity-agent-responses/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["responses"]) >= 3
    
    # Act - Filter by agent_id
    response = await client.get(f"/maturity-agent-responses/?agent_id={agent1.agent_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["responses"]) >= 2
    
    # Act - Filter by maturity_question_id
    response = await client.get(f"/maturity-agent-responses/?maturity_question_id={maturity_question1.maturity_question_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["responses"]) >= 2
