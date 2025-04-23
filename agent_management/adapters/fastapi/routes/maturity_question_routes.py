"""FastAPI routes for maturity question operations."""
from typing import Optional, Callable
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.postgres.repositories.maturity_question_repository import MaturityQuestionRepository
from adapters.postgres.config import get_session
from adapters.s3 import main as s3
from adapters.saia import saia_adapter


from domain.command.comon_command import sql, Sources

from domain.command.maturity_question_command import (
    CreateMaturityQuestion,
    UpdateMaturityQuestion,
    DeleteMaturityQuestion,
    GetMaturityQuestion,
    MaturityQuestionResponse,
    ListMaturityQuestions,
    ChatMessage,
    ChatRequest,
    ChatResponse
)
from domain.command_handlers.maturity_question_handler import (
    create_maturity_question,
    update_maturity_question,
    delete_maturity_question,
    get_maturity_question,
    list_maturity_questions,
    chat_maturity_questions
)

router = APIRouter(prefix="/maturity-questions", tags=["maturity-questions"])


async def get_maturity_question_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for maturity question handler functions.

    Args:
        session: AsyncSession from dependency injection

    Returns:
        dict[str, Callable]: Dictionary containing handler functions for maturity questions
    """
    repository = MaturityQuestionRepository(session)
    sql_object = sql(maturity_question=repository)
    sources = Sources(sql=sql_object, asistant=saia_adapter, storage=s3)
    return {
        'chat_maturity_question': lambda cmd: chat_maturity_questions(sources, cmd),
        'create_maturity_question': lambda cmd: create_maturity_question(repository, cmd),
        'update_maturity_question': lambda cmd: update_maturity_question(repository, cmd),
        'delete_maturity_question': lambda cmd: delete_maturity_question(repository, cmd),
        'get_maturity_question': lambda cmd: get_maturity_question(repository, cmd),
        'list_maturity_questions': lambda category=None, question_type=None, axis_id=None, industry_id=None: list_maturity_questions(
            repository, category, question_type, axis_id, industry_id
        )
    }

@router.post("/chat", response_model=ChatResponse)
async def chat_maturity_question_endpoint(
    command: ChatRequest,
    handler: dict[str, Callable] = Depends(get_maturity_question_handler)
):
    try:
        return await handler['chat_maturity_question'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  


@router.post("/", response_model=int)
async def create_maturity_question_endpoint(
    command: CreateMaturityQuestion,
    handler: dict[str, Callable] = Depends(get_maturity_question_handler)
):
    """
    Create a new maturity question.

    Args:
        command: CreateMaturityQuestion command with question details
        handler: Maturity question handler functions

    Returns:
        int: ID of the created maturity question

    Raises:
        HTTPException: If validation fails
    """
    try:
        return await handler['create_maturity_question'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{maturity_question_id}", response_model=bool)
async def update_maturity_question_endpoint(
    maturity_question_id: int,
    command: UpdateMaturityQuestion,
    handler: dict[str, Callable] = Depends(get_maturity_question_handler)
):
    """
    Update an existing maturity question.

    Args:
        maturity_question_id: ID of the maturity question to update
        command: UpdateMaturityQuestion command with updated question details
        handler: Maturity question handler functions

    Returns:
        bool: True if update was successful

    Raises:
        HTTPException: If maturity question not found or validation fails
    """
    command.maturity_question_id = maturity_question_id
    try:
        if not await handler['update_maturity_question'](command):
            raise HTTPException(status_code=404, detail="Maturity question not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{maturity_question_id}", response_model=bool)
async def delete_maturity_question_endpoint(
    maturity_question_id: int,
    handler: dict[str, Callable] = Depends(get_maturity_question_handler)
):
    """
    Delete a maturity question.

    Args:
        maturity_question_id: ID of the maturity question to delete
        handler: Maturity question handler functions

    Returns:
        bool: True if deletion was successful

    Raises:
        HTTPException: If maturity question not found
    """
    command = DeleteMaturityQuestion(maturity_question_id=maturity_question_id)
    if not await handler['delete_maturity_question'](command):
        raise HTTPException(status_code=404, detail="Maturity question not found")
    return True


@router.get("/{maturity_question_id}", response_model=MaturityQuestionResponse)
async def get_maturity_question_endpoint(
    maturity_question_id: int,
    handler: dict[str, Callable] = Depends(get_maturity_question_handler)
):
    """
    Get a maturity question by ID.

    Args:
        maturity_question_id: ID of the maturity question to get
        handler: Maturity question handler functions

    Returns:
        MaturityQuestionResponse: Maturity question data

    Raises:
        HTTPException: If maturity question not found
    """
    command = GetMaturityQuestion(maturity_question_id=maturity_question_id)
    maturity_question = await handler['get_maturity_question'](command)
    if not maturity_question:
        raise HTTPException(status_code=404, detail="Maturity question not found")
    return maturity_question


@router.get("/", response_model=ListMaturityQuestions)
async def list_maturity_questions_endpoint(
    category: Optional[str] = Query(None, description="Filter by category"),
    question_type: Optional[str] = Query(None, description="Filter by question type"),
    axis_id: Optional[int] = Query(None, description="Filter by axis ID"),
    industry_id: Optional[int] = Query(None, description="Filter by industry ID"),
    handler: dict[str, Callable] = Depends(get_maturity_question_handler)
):
    """
    List all maturity questions with optional filters.

    Args:
        category: Optional category filter
        question_type: Optional question type filter
        axis_id: Optional axis ID filter
        industry_id: Optional industry ID filter
        handler: Maturity question handler functions

    Returns:
        ListMaturityQuestions: List of maturity questions
    """
    return await handler['list_maturity_questions'](category, question_type, axis_id, industry_id)
