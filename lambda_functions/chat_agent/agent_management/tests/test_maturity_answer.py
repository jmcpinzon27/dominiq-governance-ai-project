"""Tests for maturity answer operations."""
import pytest
from datetime import datetime
from httpx import AsyncClient
from fastapi import FastAPI

from domain.command.maturity_answer_command import (
    CreateMaturityAnswer,
    UpdateMaturityAnswer,
    GetMaturityAnswer,
    MaturityAnswerResponse
)
from adapters.postgres.models.maturity_answer import MaturityAnswer
from adapters.postgres.models.maturity_question import MaturityQuestion
from adapters.postgres.models.session import Session
from adapters.postgres.repositories.maturity_answer_repository import MaturityAnswerRepository


@pytest.mark.asyncio
async def test_create_maturity_answer(app: FastAPI, client: AsyncClient, test_session):
    """Test creating a new maturity answer."""
    # Create test session and maturity question
    session = Session(
        user_id=1,  # Assuming user with ID 1 exists
        session_token="test_token",
        is_active=True
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question",
        question_type="multiple_choice"
    )
    test_session.add_all([session, maturity_question])
    await test_session.commit()
    await test_session.refresh(session)
    await test_session.refresh(maturity_question)
    
    # Arrange
    maturity_answer_data = {
        "session_id": session.session_id,
        "maturity_question_id": maturity_question.maturity_question_id,
        "answer_text": "Test answer",
        "answered_at": datetime.now().isoformat()
    }
    
    # Act
    response = await client.post("/maturity-answers/", json=maturity_answer_data)
    
    # Assert
    assert response.status_code == 200
    maturity_answer_id = response.json()
    assert isinstance(maturity_answer_id, int)
    
    # Verify in database
    repository = MaturityAnswerRepository(test_session)
    maturity_answer = await repository.get(
        GetMaturityAnswer(maturity_answer_id=maturity_answer_id)
    )
    assert maturity_answer is not None
    assert maturity_answer.session_id == maturity_answer_data["session_id"]
    assert maturity_answer.maturity_question_id == maturity_answer_data["maturity_question_id"]
    assert maturity_answer.answer_text == maturity_answer_data["answer_text"]


@pytest.mark.asyncio
async def test_update_maturity_answer(app: FastAPI, client: AsyncClient, test_session):
    """Test updating a maturity answer."""
    # Create test session and maturity question
    session = Session(
        user_id=1,  # Assuming user with ID 1 exists
        session_token="test_token_update",
        is_active=True
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question for update",
        question_type="multiple_choice"
    )
    test_session.add_all([session, maturity_question])
    await test_session.commit()
    await test_session.refresh(session)
    await test_session.refresh(maturity_question)
    
    # Create a maturity answer to update
    maturity_answer = MaturityAnswer(
        session_id=session.session_id,
        maturity_question_id=maturity_question.maturity_question_id,
        answer_text="Original answer"
    )
    test_session.add(maturity_answer)
    await test_session.commit()
    await test_session.refresh(maturity_answer)
    
    # Arrange
    update_data = {
        "session_id": session.session_id,
        "maturity_question_id": maturity_question.maturity_question_id,
        "answer_text": "Updated answer",
        "answered_at": datetime.now().isoformat()
    }
    
    # Act
    response = await client.put(
        f"/maturity-answers/{maturity_answer.maturity_answer_id}",
        json=update_data
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    repository = MaturityAnswerRepository(test_session)
    updated_answer = await repository.get(
        GetMaturityAnswer(maturity_answer_id=maturity_answer.maturity_answer_id)
    )
    assert updated_answer.answer_text == update_data["answer_text"]


@pytest.mark.asyncio
async def test_delete_maturity_answer(app: FastAPI, client: AsyncClient, test_session):
    """Test deleting a maturity answer."""
    # Create test session and maturity question
    session = Session(
        user_id=1,  # Assuming user with ID 1 exists
        session_token="test_token_delete",
        is_active=True
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question for delete",
        question_type="multiple_choice"
    )
    test_session.add_all([session, maturity_question])
    await test_session.commit()
    await test_session.refresh(session)
    await test_session.refresh(maturity_question)
    
    # Create a maturity answer to delete
    maturity_answer = MaturityAnswer(
        session_id=session.session_id,
        maturity_question_id=maturity_question.maturity_question_id,
        answer_text="Answer to delete"
    )
    test_session.add(maturity_answer)
    await test_session.commit()
    await test_session.refresh(maturity_answer)
    
    # Act
    response = await client.delete(
        f"/maturity-answers/{maturity_answer.maturity_answer_id}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    repository = MaturityAnswerRepository(test_session)
    deleted_answer = await repository.get(
        GetMaturityAnswer(maturity_answer_id=maturity_answer.maturity_answer_id)
    )
    assert deleted_answer is None


@pytest.mark.asyncio
async def test_get_maturity_answer(app: FastAPI, client: AsyncClient, test_session):
    """Test getting a maturity answer by ID."""
    # Create test session and maturity question
    session = Session(
        user_id=1,  # Assuming user with ID 1 exists
        session_token="test_token_get",
        is_active=True
    )
    maturity_question = MaturityQuestion(
        question_text="Test maturity question for get",
        question_type="multiple_choice"
    )
    test_session.add_all([session, maturity_question])
    await test_session.commit()
    await test_session.refresh(session)
    await test_session.refresh(maturity_question)
    
    # Create a maturity answer to get
    maturity_answer = MaturityAnswer(
        session_id=session.session_id,
        maturity_question_id=maturity_question.maturity_question_id,
        answer_text="Answer to get"
    )
    test_session.add(maturity_answer)
    await test_session.commit()
    await test_session.refresh(maturity_answer)
    
    # Act
    response = await client.get(
        f"/maturity-answers/{maturity_answer.maturity_answer_id}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["maturity_answer_id"] == maturity_answer.maturity_answer_id
    assert data["session_id"] == maturity_answer.session_id
    assert data["maturity_question_id"] == maturity_answer.maturity_question_id
    assert data["answer_text"] == maturity_answer.answer_text


@pytest.mark.asyncio
async def test_list_maturity_answers(app: FastAPI, client: AsyncClient, test_session):
    """Test listing maturity answers with filters."""
    # Create test session and maturity questions
    session = Session(
        user_id=1,  # Assuming user with ID 1 exists
        session_token="test_token_list",
        is_active=True
    )
    maturity_question1 = MaturityQuestion(
        question_text="Test maturity question 1",
        question_type="multiple_choice"
    )
    maturity_question2 = MaturityQuestion(
        question_text="Test maturity question 2",
        question_type="free_text"
    )
    test_session.add_all([session, maturity_question1, maturity_question2])
    await test_session.commit()
    await test_session.refresh(session)
    await test_session.refresh(maturity_question1)
    await test_session.refresh(maturity_question2)
    
    # Create maturity answers
    maturity_answers = [
        MaturityAnswer(
            session_id=session.session_id,
            maturity_question_id=maturity_question1.maturity_question_id,
            answer_text="Answer 1"
        ),
        MaturityAnswer(
            session_id=session.session_id,
            maturity_question_id=maturity_question2.maturity_question_id,
            answer_text="Answer 2"
        )
    ]
    for answer in maturity_answers:
        test_session.add(answer)
    await test_session.commit()
    
    # Act - Get all answers
    response = await client.get("/maturity-answers/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["answers"]) >= 2
    
    # Act - Filter by session_id
    response = await client.get(f"/maturity-answers/?session_id={session.session_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["answers"]) >= 2
    
    # Act - Filter by maturity_question_id
    response = await client.get(f"/maturity-answers/?maturity_question_id={maturity_question1.maturity_question_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["answers"]) >= 1
    assert data["answers"][0]["maturity_question_id"] == maturity_question1.maturity_question_id
