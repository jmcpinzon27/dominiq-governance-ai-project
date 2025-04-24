"""FastAPI routes for maturity answer operations."""
from typing import Optional, Callable
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.maturity_answer_command import (
    CreateMaturityAnswer,
    UpdateMaturityAnswer,
    DeleteMaturityAnswer,
    GetMaturityAnswer,
    MaturityAnswerResponse,
    ListMaturityAnswers
)
from domain.command_handlers.maturity_answer_handler import (
    create_maturity_answer,
    update_maturity_answer,
    delete_maturity_answer,
    get_maturity_answer,
    list_maturity_answers
)
from adapters.postgres.repositories.maturity_answer_repository import MaturityAnswerRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/maturity-answers", tags=["maturity-answers"])


async def get_maturity_answer_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for maturity answer handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for maturity answers
    """
    repository = MaturityAnswerRepository(session)
    return {
        'create_maturity_answer': lambda cmd: create_maturity_answer(repository, cmd),
        'update_maturity_answer': lambda cmd: update_maturity_answer(repository, cmd),
        'delete_maturity_answer': lambda cmd: delete_maturity_answer(repository, cmd),
        'get_maturity_answer': lambda cmd: get_maturity_answer(repository, cmd),
        'list_maturity_answers': lambda session_id=None, maturity_question_id=None: 
            list_maturity_answers(repository, session_id, maturity_question_id)
    }


@router.post("/", response_model=int)
async def create_maturity_answer_endpoint(
    command: CreateMaturityAnswer,
    handler: dict[str, Callable] = Depends(get_maturity_answer_handler)
):
    """
    Create a new maturity answer.
    
    Args:
        command: CreateMaturityAnswer command with answer details
        handler: Maturity answer handler functions
        
    Returns:
        int: ID of the created maturity answer
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        return await handler['create_maturity_answer'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{maturity_answer_id}", response_model=bool)
async def update_maturity_answer_endpoint(
    maturity_answer_id: int,
    command: UpdateMaturityAnswer,
    handler: dict[str, Callable] = Depends(get_maturity_answer_handler)
):
    """
    Update an existing maturity answer.
    
    Args:
        maturity_answer_id: ID of the maturity answer to update
        command: UpdateMaturityAnswer command with updated answer details
        handler: Maturity answer handler functions
        
    Returns:
        bool: True if update was successful
        
    Raises:
        HTTPException: If maturity answer not found or validation fails
    """
    command.maturity_answer_id = maturity_answer_id
    try:
        if not await handler['update_maturity_answer'](command):
            raise HTTPException(status_code=404, detail="Maturity answer not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{maturity_answer_id}", response_model=bool)
async def delete_maturity_answer_endpoint(
    maturity_answer_id: int,
    handler: dict[str, Callable] = Depends(get_maturity_answer_handler)
):
    """
    Delete a maturity answer.
    
    Args:
        maturity_answer_id: ID of the maturity answer to delete
        handler: Maturity answer handler functions
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If maturity answer not found
    """
    if not await handler['delete_maturity_answer'](DeleteMaturityAnswer(maturity_answer_id=maturity_answer_id)):
        raise HTTPException(status_code=404, detail="Maturity answer not found")
    return True


@router.get("/{maturity_answer_id}", response_model=MaturityAnswerResponse)
async def get_maturity_answer_endpoint(
    maturity_answer_id: int,
    handler: dict[str, Callable] = Depends(get_maturity_answer_handler)
):
    """
    Get a maturity answer by ID.
    
    Args:
        maturity_answer_id: ID of the maturity answer to get
        handler: Maturity answer handler functions
        
    Returns:
        MaturityAnswerResponse: Maturity answer data
        
    Raises:
        HTTPException: If maturity answer not found
    """
    answer = await handler['get_maturity_answer'](GetMaturityAnswer(maturity_answer_id=maturity_answer_id))
    if not answer:
        raise HTTPException(status_code=404, detail="Maturity answer not found")
    return answer


@router.get("/", response_model=ListMaturityAnswers)
async def list_maturity_answers_endpoint(
    session_id: Optional[int] = Query(None, description="Filter by session ID"),
    maturity_question_id: Optional[int] = Query(None, description="Filter by maturity question ID"),
    handler: dict[str, Callable] = Depends(get_maturity_answer_handler)
):
    """
    List all maturity answers, optionally filtered by session_id or maturity_question_id.
    
    Args:
        session_id: Optional session ID filter
        maturity_question_id: Optional maturity question ID filter
        handler: Maturity answer handler functions
        
    Returns:
        ListMaturityAnswers: List of maturity answers
    """
    return await handler['list_maturity_answers'](session_id, maturity_question_id)
