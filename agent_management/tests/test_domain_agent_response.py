"""Tests for domain agent response operations."""
import pytest
from datetime import datetime
from httpx import AsyncClient
from fastapi import FastAPI

from domain.command.domain_agent_response_command import (
    CreateDomainAgentResponse,
    UpdateDomainAgentResponse,
    GetDomainAgentResponse,
    DomainAgentResponseData
)
from adapters.postgres.models.domain_agent_response import DomainAgentResponse
from adapters.postgres.models.domain_question import DomainQuestion
from adapters.postgres.models.domain import Domain
from adapters.postgres.models.agent import Agent
from adapters.postgres.repositories.domain_agent_response_repository import DomainAgentResponseRepository


@pytest.mark.asyncio
async def test_create_domain_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test creating a new domain agent response."""
    # Create test agent and domain question
    agent = Agent(
        agent_name="Test Agent",
        agent_role="Test Role"
    )
    domain = Domain(
        domain_name="Test Domain",
        company_id=1  # Assuming company with ID 1 exists
    )
    test_session.add_all([agent, domain])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(domain)
    
    domain_question = DomainQuestion(
        domain_id=domain.domain_id,
        question_text="Test domain question",
        question_type="multiple_choice"
    )
    test_session.add(domain_question)
    await test_session.commit()
    await test_session.refresh(domain_question)
    
    # Arrange
    domain_agent_response_data = {
        "agent_id": agent.agent_id,
        "domain_question_id": domain_question.domain_question_id,
        "response_text": "Test response",
        "response_date": datetime.now().isoformat()
    }
    
    # Act
    response = await client.post("/domain-agent-responses/", json=domain_agent_response_data)
    
    # Assert
    assert response.status_code == 200
    domain_agent_response_id = response.json()
    assert isinstance(domain_agent_response_id, int)
    
    # Verify in database
    repository = DomainAgentResponseRepository(test_session)
    domain_agent_response = await repository.get(
        GetDomainAgentResponse(domain_agent_response_id=domain_agent_response_id)
    )
    assert domain_agent_response is not None
    assert domain_agent_response.agent_id == domain_agent_response_data["agent_id"]
    assert domain_agent_response.domain_question_id == domain_agent_response_data["domain_question_id"]
    assert domain_agent_response.response_text == domain_agent_response_data["response_text"]


@pytest.mark.asyncio
async def test_update_domain_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test updating a domain agent response."""
    # Create test agent and domain question
    agent = Agent(
        agent_name="Test Agent for Update",
        agent_role="Test Role"
    )
    domain = Domain(
        domain_name="Test Domain for Update",
        company_id=1  # Assuming company with ID 1 exists
    )
    test_session.add_all([agent, domain])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(domain)
    
    domain_question = DomainQuestion(
        domain_id=domain.domain_id,
        question_text="Test domain question for update",
        question_type="multiple_choice"
    )
    test_session.add(domain_question)
    await test_session.commit()
    await test_session.refresh(domain_question)
    
    # Create a domain agent response to update
    domain_agent_response = DomainAgentResponse(
        agent_id=agent.agent_id,
        domain_question_id=domain_question.domain_question_id,
        response_text="Original response"
    )
    test_session.add(domain_agent_response)
    await test_session.commit()
    await test_session.refresh(domain_agent_response)
    
    # Arrange
    update_data = {
        "agent_id": agent.agent_id,
        "domain_question_id": domain_question.domain_question_id,
        "response_text": "Updated response",
        "response_date": datetime.now().isoformat()
    }
    
    # Act
    response = await client.put(
        f"/domain-agent-responses/{domain_agent_response.domain_agent_response_id}",
        json=update_data
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    repository = DomainAgentResponseRepository(test_session)
    updated_response = await repository.get(
        GetDomainAgentResponse(domain_agent_response_id=domain_agent_response.domain_agent_response_id)
    )
    assert updated_response.response_text == update_data["response_text"]


@pytest.mark.asyncio
async def test_delete_domain_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test deleting a domain agent response."""
    # Create test agent and domain question
    agent = Agent(
        agent_name="Test Agent for Delete",
        agent_role="Test Role"
    )
    domain = Domain(
        domain_name="Test Domain for Delete",
        company_id=1  # Assuming company with ID 1 exists
    )
    test_session.add_all([agent, domain])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(domain)
    
    domain_question = DomainQuestion(
        domain_id=domain.domain_id,
        question_text="Test domain question for delete",
        question_type="multiple_choice"
    )
    test_session.add(domain_question)
    await test_session.commit()
    await test_session.refresh(domain_question)
    
    # Create a domain agent response to delete
    domain_agent_response = DomainAgentResponse(
        agent_id=agent.agent_id,
        domain_question_id=domain_question.domain_question_id,
        response_text="Response to delete"
    )
    test_session.add(domain_agent_response)
    await test_session.commit()
    await test_session.refresh(domain_agent_response)
    
    # Act
    response = await client.delete(
        f"/domain-agent-responses/{domain_agent_response.domain_agent_response_id}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    repository = DomainAgentResponseRepository(test_session)
    deleted_response = await repository.get(
        GetDomainAgentResponse(domain_agent_response_id=domain_agent_response.domain_agent_response_id)
    )
    assert deleted_response is None


@pytest.mark.asyncio
async def test_get_domain_agent_response(app: FastAPI, client: AsyncClient, test_session):
    """Test getting a domain agent response by ID."""
    # Create test agent and domain question
    agent = Agent(
        agent_name="Test Agent for Get",
        agent_role="Test Role"
    )
    domain = Domain(
        domain_name="Test Domain for Get",
        company_id=1  # Assuming company with ID 1 exists
    )
    test_session.add_all([agent, domain])
    await test_session.commit()
    await test_session.refresh(agent)
    await test_session.refresh(domain)
    
    domain_question = DomainQuestion(
        domain_id=domain.domain_id,
        question_text="Test domain question for get",
        question_type="multiple_choice"
    )
    test_session.add(domain_question)
    await test_session.commit()
    await test_session.refresh(domain_question)
    
    # Create a domain agent response to get
    domain_agent_response = DomainAgentResponse(
        agent_id=agent.agent_id,
        domain_question_id=domain_question.domain_question_id,
        response_text="Response to get"
    )
    test_session.add(domain_agent_response)
    await test_session.commit()
    await test_session.refresh(domain_agent_response)
    
    # Act
    response = await client.get(
        f"/domain-agent-responses/{domain_agent_response.domain_agent_response_id}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["domain_agent_response_id"] == domain_agent_response.domain_agent_response_id
    assert data["agent_id"] == domain_agent_response.agent_id
    assert data["domain_question_id"] == domain_agent_response.domain_question_id
    assert data["response_text"] == domain_agent_response.response_text


@pytest.mark.asyncio
async def test_list_domain_agent_responses(app: FastAPI, client: AsyncClient, test_session):
    """Test listing domain agent responses with filters."""
    # Create test agents and domain questions
    agent1 = Agent(agent_name="Test Agent 1", agent_role="Test Role")
    agent2 = Agent(agent_name="Test Agent 2", agent_role="Test Role")
    domain = Domain(
        domain_name="Test Domain for List",
        company_id=1  # Assuming company with ID 1 exists
    )
    test_session.add_all([agent1, agent2, domain])
    await test_session.commit()
    await test_session.refresh(agent1)
    await test_session.refresh(agent2)
    await test_session.refresh(domain)
    
    domain_question1 = DomainQuestion(
        domain_id=domain.domain_id,
        question_text="Test domain question 1",
        question_type="multiple_choice"
    )
    domain_question2 = DomainQuestion(
        domain_id=domain.domain_id,
        question_text="Test domain question 2",
        question_type="free_text"
    )
    test_session.add_all([domain_question1, domain_question2])
    await test_session.commit()
    await test_session.refresh(domain_question1)
    await test_session.refresh(domain_question2)
    
    # Create domain agent responses
    domain_agent_responses = [
        DomainAgentResponse(
            agent_id=agent1.agent_id,
            domain_question_id=domain_question1.domain_question_id,
            response_text="Response 1"
        ),
        DomainAgentResponse(
            agent_id=agent1.agent_id,
            domain_question_id=domain_question2.domain_question_id,
            response_text="Response 2"
        ),
        DomainAgentResponse(
            agent_id=agent2.agent_id,
            domain_question_id=domain_question1.domain_question_id,
            response_text="Response 3"
        )
    ]
    for response in domain_agent_responses:
        test_session.add(response)
    await test_session.commit()
    
    # Act - Get all responses
    response = await client.get("/domain-agent-responses/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["responses"]) >= 3
    
    # Act - Filter by agent_id
    response = await client.get(f"/domain-agent-responses/?agent_id={agent1.agent_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["responses"]) >= 2
    
    # Act - Filter by domain_question_id
    response = await client.get(f"/domain-agent-responses/?domain_question_id={domain_question1.domain_question_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["responses"]) >= 2
