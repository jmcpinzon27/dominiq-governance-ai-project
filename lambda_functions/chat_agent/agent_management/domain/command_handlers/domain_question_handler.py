"""Handler for domain question-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.domain_question_command import (
    CreateDomainQuestion,
    UpdateDomainQuestion,
    DeleteDomainQuestion,
    GetDomainQuestion,
    DomainQuestionResponse,
    ListDomainQuestions
)


async def create_domain_question(repository: Callable, command: CreateDomainQuestion) -> int:
    """Create a new domain question."""
    return await repository.create(command)


async def update_domain_question(repository: Callable, command: UpdateDomainQuestion) -> bool:
    """Update an existing domain question."""
    return await repository.update(command)


async def delete_domain_question(repository: Callable, command: DeleteDomainQuestion) -> bool:
    """Delete a domain question."""
    return await repository.delete(command.domain_question_id)


async def get_domain_question(repository: Callable, command: GetDomainQuestion) -> Optional[DomainQuestionResponse]:
    """Retrieve a domain question by ID or filters."""
    return await repository.get(command)


async def list_domain_questions(
    repository: Callable,
    domain_id: Optional[int] = None,
    industry_id: Optional[int] = None,
    category: Optional[str] = None,
    question_type: Optional[str] = None
) -> ListDomainQuestions:
    """List all domain questions, optionally filtered."""
    questions = await repository.list_all(domain_id, industry_id, category, question_type)
    return ListDomainQuestions(questions=questions)


def create_domain_question_handler(repository: Callable) -> dict:
    """Create a dictionary of domain question handler functions."""
    return {
        'create_domain_question': partial(create_domain_question, repository),
        'update_domain_question': partial(update_domain_question, repository),
        'delete_domain_question': partial(delete_domain_question, repository),
        'get_domain_question': partial(get_domain_question, repository),
        'list_domain_questions': partial(list_domain_questions, repository),
    }
