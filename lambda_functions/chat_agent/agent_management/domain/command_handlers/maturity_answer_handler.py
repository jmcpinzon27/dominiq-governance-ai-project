"""Handler for maturity answer-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.maturity_answer_command import (
    CreateMaturityAnswer,
    UpdateMaturityAnswer,
    DeleteMaturityAnswer,
    GetMaturityAnswer,
    MaturityAnswerResponse,
    ListMaturityAnswers
)


async def create_maturity_answer(repository: Callable, command: CreateMaturityAnswer) -> int:
    """Create a new maturity answer.
    
    Args:
        repository: MaturityAnswer repository
        command: CreateMaturityAnswer command
        
    Returns:
        int: ID of the created maturity answer
    """
    return await repository.create(command)


async def update_maturity_answer(repository: Callable, command: UpdateMaturityAnswer) -> bool:
    """Update an existing maturity answer.
    
    Args:
        repository: MaturityAnswer repository
        command: UpdateMaturityAnswer command
        
    Returns:
        bool: True if update was successful
    """
    return await repository.update(command)


async def delete_maturity_answer(repository: Callable, command: DeleteMaturityAnswer) -> bool:
    """Delete a maturity answer.
    
    Args:
        repository: MaturityAnswer repository
        command: DeleteMaturityAnswer command
        
    Returns:
        bool: True if deletion was successful
    """
    return await repository.delete(command.maturity_answer_id)


async def get_maturity_answer(repository: Callable, command: GetMaturityAnswer) -> Optional[MaturityAnswerResponse]:
    """Retrieve a maturity answer by ID or filters.
    
    Args:
        repository: MaturityAnswer repository
        command: GetMaturityAnswer command
        
    Returns:
        Optional[MaturityAnswerResponse]: Maturity answer data if found, None otherwise
    """
    return await repository.get(command)


async def list_maturity_answers(
    repository: Callable,
    session_id: Optional[int] = None,
    maturity_question_id: Optional[int] = None
) -> ListMaturityAnswers:
    """List all maturity answers, optionally filtered.
    
    Args:
        repository: MaturityAnswer repository
        session_id: Optional session ID filter
        maturity_question_id: Optional maturity question ID filter
        
    Returns:
        ListMaturityAnswers: List of maturity answers
    """
    answers = await repository.list_all(session_id, maturity_question_id)
    return ListMaturityAnswers(answers=answers)


def create_maturity_answer_handler(repository: Callable) -> dict:
    """Create a dictionary of maturity answer-related functions with bound repository.
    
    Args:
        repository: MaturityAnswer repository
        
    Returns:
        dict: Dictionary of handler functions
    """
    return {
        'create_maturity_answer': partial(create_maturity_answer, repository),
        'update_maturity_answer': partial(update_maturity_answer, repository),
        'delete_maturity_answer': partial(delete_maturity_answer, repository),
        'get_maturity_answer': partial(get_maturity_answer, repository),
        'list_maturity_answers': partial(list_maturity_answers, repository),
    }
