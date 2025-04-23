"""FastAPI routes for domain question operations."""
from typing import Optional, Callable
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.domain_question_command import (
    CreateDomainQuestion,
    UpdateDomainQuestion,
    DeleteDomainQuestion,
    GetDomainQuestion,
    DomainQuestionResponse,
    ListDomainQuestions
)
from domain.command_handlers.domain_question_handler import (
    create_domain_question,
    update_domain_question,
    delete_domain_question,
    get_domain_question,
    list_domain_questions
)
from adapters.postgres.repositories.domain_question_repository import DomainQuestionRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/domain-questions", tags=["domain-questions"])


async def get_domain_question_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for domain question handler functions.

    Args:
        session: AsyncSession from dependency injection

    Returns:
        dict[str, Callable]: Dictionary containing handler functions for domain questions
    """
    repository = DomainQuestionRepository(session)
    return {
        'create_domain_question': lambda cmd: create_domain_question(repository, cmd),
        'update_domain_question': lambda cmd: update_domain_question(repository, cmd),
        'delete_domain_question': lambda cmd: delete_domain_question(repository, cmd),
        'get_domain_question': lambda cmd: get_domain_question(repository, cmd),
        'list_domain_questions': lambda domain_id=None, industry_id=None, category=None, question_type=None:
            list_domain_questions(repository, domain_id, industry_id, category, question_type)
    }


@router.post("/", response_model=int)
async def create_domain_question_route(
    command: CreateDomainQuestion,
    handler: dict[str, Callable] = Depends(get_domain_question_handler)
):
    """Create a new domain question."""
    return await handler['create_domain_question'](command)


@router.put("/{domain_question_id}", response_model=bool)
async def update_domain_question_route(
    domain_question_id: int,
    command: UpdateDomainQuestion,
    handler: dict[str, Callable] = Depends(get_domain_question_handler)
):
    """Update an existing domain question."""
    command.domain_question_id = domain_question_id
    if not await handler['update_domain_question'](command):
        raise HTTPException(status_code=404, detail="Domain question not found")
    return True


@router.delete("/{domain_question_id}", response_model=bool)
async def delete_domain_question_route(
    domain_question_id: int,
    handler: dict[str, Callable] = Depends(get_domain_question_handler)
):
    """Delete a domain question."""
    if not await handler['delete_domain_question'](
        DeleteDomainQuestion(domain_question_id=domain_question_id)
    ):
        raise HTTPException(status_code=404, detail="Domain question not found")
    return True


@router.get("/{domain_question_id}", response_model=DomainQuestionResponse)
async def get_domain_question_route(
    domain_question_id: int,
    handler: dict[str, Callable] = Depends(get_domain_question_handler)
):
    """Get a domain question by ID."""
    question = await handler['get_domain_question'](
        GetDomainQuestion(domain_question_id=domain_question_id)
    )
    if not question:
        raise HTTPException(status_code=404, detail="Domain question not found")
    return question


@router.get("/", response_model=ListDomainQuestions)
async def list_domain_questions_route(
    domain_id: Optional[int] = Query(None, description="Filter by domain ID"),
    industry_id: Optional[int] = Query(None, description="Filter by industry ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    question_type: Optional[str] = Query(None, description="Filter by question type"),
    handler: dict[str, Callable] = Depends(get_domain_question_handler)
):
    """List all domain questions with optional filters."""
    return await handler['list_domain_questions'](domain_id, industry_id, category, question_type)
