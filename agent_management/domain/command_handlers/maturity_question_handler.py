"""Handler for maturity question-related commands."""
import json
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional, List, Callable, Dict
from functools import partial

from domain.command.comon_command import Sources 
from domain.command.maturity_question_command import (
    Question, QuestionOption,
    MaturityQuestionBase,
    CreateMaturityQuestion,
    UpdateMaturityQuestion,
    DeleteMaturityQuestion,
    GetMaturityQuestion,
    MaturityQuestionResponse,
    ListMaturityQuestions,
    ChatResponse
)


async def create_maturity_question(repository: Callable, command: CreateMaturityQuestion) -> int:
    """Create a new maturity question.

    Args:
        repository: MaturityQuestion repository
        command: CreateMaturityQuestion command

    Returns:
        int: ID of the created maturity question
    """
    return await repository.create(command)


async def update_maturity_question(repository: Callable, command: UpdateMaturityQuestion) -> bool:
    """Update an existing maturity question.

    Args:
        repository: MaturityQuestion repository
        command: UpdateMaturityQuestion command

    Returns:
        bool: True if update was successful
    """
    return await repository.update(command)


async def delete_maturity_question(repository: Callable, command: DeleteMaturityQuestion) -> bool:
    """Delete a maturity question.

    Args:
        repository: MaturityQuestion repository
        command: DeleteMaturityQuestion command

    Returns:
        bool: True if deletion was successful
    """
    return await repository.delete(command.maturity_question_id)


async def get_maturity_question(repository: Callable, command: GetMaturityQuestion) -> Optional[MaturityQuestionResponse]:
    """Retrieve a maturity question by ID or filters.

    Args:
        repository: MaturityQuestion repository
        command: GetMaturityQuestion command

    Returns:
        Optional[MaturityQuestionResponse]: Maturity question data if found, None otherwise
    """
    return await repository.get(command)


async def list_maturity_questions(
    repository: Callable,
    category: Optional[str] = None,
    question_type: Optional[str] = None,
    axis_id: Optional[int] = None,
    industry_id: Optional[int] = None
) -> ListMaturityQuestions:
    """List all maturity questions, optionally filtered.

    Args:
        repository: MaturityQuestion repository
        category: Optional category filter
        question_type: Optional question type filter
        axis_id: Optional axis ID filter
        industry_id: Optional industry ID filter

    Returns:
        ListMaturityQuestions: List of maturity questions
    """
    questions = await repository.list_all(category, question_type, axis_id, industry_id)
    return ListMaturityQuestions(questions=questions)


async def chat_maturity_questions(sources: Sources, cmd):
    session_file_content = sources.storage.download_session_data(f"{cmd.session_id}.pkl")
    
        # Create or load state
    state = None
    if session_file_content:
        state = sources.asistant.load_survey_state(session_file_content)

    if not state:
        questions: Question = await sources.sql.maturity_question.get_questions_with_response(
            axis_id=cmd.axis_id
        )
        state = await sources.asistant.initialize_survey(user_id=cmd.session_id, questions=questions)

    state, response = await sources.asistant.process_response(
        state,
        cmd.input_text
    )
    session_file_content = sources.asistant.save_survey_state(state)
    sources.storage.upload_session_data(session_file_content, f"{cmd.session_id}.pkl")
    return ChatResponse(
        messages=response,
        timestamp=pd.Timestamp.now().isoformat()
    )


def create_maturity_question_handler(repository: Callable) -> dict:
    """Create a dictionary of maturity question handler functions.

    Args:
        repository: MaturityQuestion repository

    Returns:
        dict: Dictionary of handler functions
    """
    return {
        'create_maturity_question': partial(create_maturity_question, repository),
        'update_maturity_question': partial(update_maturity_question, repository),
        'delete_maturity_question': partial(delete_maturity_question, repository),
        'get_maturity_question': partial(get_maturity_question, repository),
        'list_maturity_questions': partial(list_maturity_questions, repository),
    }
