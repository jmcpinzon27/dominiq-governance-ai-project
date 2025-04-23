"""Tests for domain question operations with industry relationship."""
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from domain.command.domain_question_command import CreateDomainQuestion, UpdateDomainQuestion
from domain.command.industry_command import CreateIndustry
from adapters.postgres.models.domain_question import DomainQuestion
from adapters.postgres.models.domain import Domain
from adapters.postgres.models.industry import Industry
from adapters.postgres.repositories.domain_question_repository import DomainQuestionRepository
from adapters.postgres.repositories.industry_repository import IndustryRepository


@pytest.mark.asyncio
async def test_create_domain_question_with_industry(app: FastAPI, client: AsyncClient, test_session):
    """Test creating a domain question with industry relationship."""
    # Create a test industry
    industry_repo = IndustryRepository(test_session)
    industry_data = CreateIndustry(
        industry_name="Test Industry",
        description="Test industry description"
    )
    industry_id = await industry_repo.create(industry_data)
    
    # Create a test domain
    domain = Domain(
        domain_name="Test Domain",
        company_id=1  # Assuming company with ID 1 exists
    )
    test_session.add(domain)
    await test_session.commit()
    await test_session.refresh(domain)
    
    # Create a domain question with industry
    domain_question_data = {
        "domain_id": domain.domain_id,
        "industry_id": industry_id,
        "question_text": "Test question with industry",
        "question_type": "multiple_choice",
        "category": "Test Category"
    }
    
    response = await client.post("/domain-questions/", json=domain_question_data)
    
    # Assert
    assert response.status_code == 200
    domain_question_id = response.json()
    
    # Verify in database
    repository = DomainQuestionRepository(test_session)
    domain_question = await repository.get_by_id(domain_question_id)
    assert domain_question is not None
    assert domain_question.industry_id == industry_id


@pytest.mark.asyncio
async def test_filter_domain_questions_by_industry(app: FastAPI, client: AsyncClient, test_session):
    """Test filtering domain questions by industry."""
    # Create test industries
    industry_repo = IndustryRepository(test_session)
    industry1_data = CreateIndustry(industry_name="Industry 1", description="Description 1")
    industry2_data = CreateIndustry(industry_name="Industry 2", description="Description 2")
    industry1_id = await industry_repo.create(industry1_data)
    industry2_id = await industry_repo.create(industry2_data)
    
    # Create a test domain
    domain = Domain(
        domain_name="Test Domain for Industry Filter",
        company_id=1  # Assuming company with ID 1 exists
    )
    test_session.add(domain)
    await test_session.commit()
    await test_session.refresh(domain)
    
    # Create domain questions with different industries
    domain_question1 = DomainQuestion(
        domain_id=domain.domain_id,
        industry_id=industry1_id,
        question_text="Question for Industry 1",
        question_type="multiple_choice",
        category="Test"
    )
    domain_question2 = DomainQuestion(
        domain_id=domain.domain_id,
        industry_id=industry2_id,
        question_text="Question for Industry 2",
        question_type="multiple_choice",
        category="Test"
    )
    domain_question3 = DomainQuestion(
        domain_id=domain.domain_id,
        industry_id=industry1_id,
        question_text="Another Question for Industry 1",
        question_type="free_text",
        category="Test"
    )
    
    test_session.add_all([domain_question1, domain_question2, domain_question3])
    await test_session.commit()
    
    # Test filtering by industry1
    response = await client.get(f"/domain-questions/?industry_id={industry1_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 2
    question_texts = [q["question_text"] for q in data["questions"]]
    assert "Question for Industry 1" in question_texts
    assert "Another Question for Industry 1" in question_texts
    assert "Question for Industry 2" not in question_texts
    
    # Test filtering by industry2
    response = await client.get(f"/domain-questions/?industry_id={industry2_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 1
    assert data["questions"][0]["question_text"] == "Question for Industry 2"
