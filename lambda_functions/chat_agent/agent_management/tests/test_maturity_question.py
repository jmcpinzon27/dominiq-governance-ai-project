"""Tests for maturity question operations."""
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from domain.command.maturity_question_command import (
    CreateMaturityQuestion,
    UpdateMaturityQuestion,
    GetMaturityQuestion,
    MaturityQuestionResponse
)
from adapters.postgres.models.maturity_question import MaturityQuestion
from adapters.postgres.repositories.maturity_question_repository import MaturityQuestionRepository


@pytest.mark.asyncio
async def test_create_maturity_question(app: FastAPI, client: AsyncClient, test_session):
    """Test creating a new maturity question."""
    # Arrange
    maturity_question_data = {
        "question_text": "Test maturity question",
        "question_type": "multiple_choice",
        "question_order": 1,
        "category": "Test Category"
    }

    # Act
    response = await client.post("/maturity-questions/", json=maturity_question_data)

    # Assert
    assert response.status_code == 200
    maturity_question_id = response.json()
    assert isinstance(maturity_question_id, int)

    # Verify in database
    repository = MaturityQuestionRepository(test_session)
    maturity_question = await repository.get(
        GetMaturityQuestion(maturity_question_id=maturity_question_id)
    )
    assert maturity_question is not None
    assert maturity_question.question_text == maturity_question_data["question_text"]
    assert maturity_question.question_type == maturity_question_data["question_type"]
    assert maturity_question.question_order == maturity_question_data["question_order"]
    assert maturity_question.category == maturity_question_data["category"]


@pytest.mark.asyncio
async def test_update_maturity_question(app: FastAPI, client: AsyncClient, test_session):
    """Test updating a maturity question."""
    # Arrange
    repository = MaturityQuestionRepository(test_session)
    maturity_question = MaturityQuestion(
        question_text="Original maturity question",
        question_type="multiple_choice",
        question_order=1,
        category="Original Category"
    )
    test_session.add(maturity_question)
    await test_session.commit()
    await test_session.refresh(maturity_question)

    update_data = {
        "question_text": "Updated maturity question",
        "question_type": "free_text",
        "question_order": 2,
        "category": "Updated Category"
    }

    # Act
    response = await client.put(
        f"/maturity-questions/{maturity_question.maturity_question_id}",
        json=update_data
    )

    # Assert
    assert response.status_code == 200
    assert response.json() is True

    # Verify in database
    updated_question = await repository.get(
        GetMaturityQuestion(maturity_question_id=maturity_question.maturity_question_id)
    )
    assert updated_question.question_text == update_data["question_text"]
    assert updated_question.question_type == update_data["question_type"]
    assert updated_question.question_order == update_data["question_order"]
    assert updated_question.category == update_data["category"]


@pytest.mark.asyncio
async def test_delete_maturity_question(app: FastAPI, client: AsyncClient, test_session):
    """Test deleting a maturity question."""
    # Arrange
    repository = MaturityQuestionRepository(test_session)
    maturity_question = MaturityQuestion(
        question_text="Maturity question to delete",
        question_type="multiple_choice",
        category="Test Category"
    )
    test_session.add(maturity_question)
    await test_session.commit()
    await test_session.refresh(maturity_question)

    # Act
    response = await client.delete(
        f"/maturity-questions/{maturity_question.maturity_question_id}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() is True

    # Verify in database
    deleted_question = await repository.get(
        GetMaturityQuestion(maturity_question_id=maturity_question.maturity_question_id)
    )
    assert deleted_question is None


@pytest.mark.asyncio
async def test_get_maturity_question(app: FastAPI, client: AsyncClient, test_session):
    """Test getting a maturity question by ID."""
    # Arrange
    maturity_question = MaturityQuestion(
        question_text="Maturity question to get",
        question_type="multiple_choice",
        category="Test Category"
    )
    test_session.add(maturity_question)
    await test_session.commit()
    await test_session.refresh(maturity_question)

    # Act
    response = await client.get(
        f"/maturity-questions/{maturity_question.maturity_question_id}"
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["maturity_question_id"] == maturity_question.maturity_question_id
    assert data["question_text"] == maturity_question.question_text
    assert data["question_type"] == maturity_question.question_type
    assert data["category"] == maturity_question.category


@pytest.mark.asyncio
async def test_list_maturity_questions(app: FastAPI, client: AsyncClient, test_session):
    """Test listing maturity questions with filters."""
    # Arrange
    maturity_questions = [
        MaturityQuestion(
            question_text="Maturity question 1",
            question_type="multiple_choice",
            category="Category A"
        ),
        MaturityQuestion(
            question_text="Maturity question 2",
            question_type="free_text",
            category="Category B"
        ),
        MaturityQuestion(
            question_text="Maturity question 3",
            question_type="multiple_choice",
            category="Category A"
        )
    ]
    for q in maturity_questions:
        test_session.add(q)
    await test_session.commit()

    # Act - Get all questions
    response = await client.get("/maturity-questions/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 3

    # Act - Filter by category
    response = await client.get("/maturity-questions/?category=Category%20A")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 2

    # Act - Filter by question_type
    response = await client.get("/maturity-questions/?question_type=free_text")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 1
    assert data["questions"][0]["question_text"] == "Maturity question 2"
