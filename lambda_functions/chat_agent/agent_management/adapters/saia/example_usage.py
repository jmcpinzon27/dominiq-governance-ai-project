"""
Example usage of the SAIA.ai LangChain adapter.

This module demonstrates how to use the SAIA.ai LangChain adapter
for survey applications with maturity questions.
"""
import asyncio
from typing import Optional

from adapters.postgres.repositories.maturity_question_repository import MaturityQuestionRepository
from adapters.langchain.saia_adapter import (
    process_survey_interaction,
    create_survey_state,
    load_questions_from_repository,
    validate_response,
    load_history,
    dump_history,
    Question
)


async def run_survey_example(session, axis_id: Optional[int] = None):
    """
    Run an example survey using the SAIA.ai LangChain adapter.

    Args:
        session: SQLAlchemy session
        axis_id: Optional axis ID filter
    """
    # Create repository
    repository = MaturityQuestionRepository(session)

    # Load questions
    questions = await load_questions_from_repository(repository, axis_id=axis_id)

    # Print loaded questions
    print(f"Loaded {len(questions)} questions")
    for i, question in enumerate(questions):
        print(f"Question {i+1}: {question.question_text}")
        if question.options:
            print("Options:")
            for opt in question.options:
                print(f"  {opt.id}: {opt.text}")
        print()

    # Create survey state
    state = await create_survey_state(repository, axis_id=axis_id)

    # Example of processing a message
    new_state, response = await process_survey_interaction(
        repository,
        "Hello, I'm ready to take the survey",
        user_id="example_user"
    )
    print(f"Assistant: {response.messages.content}")

    # Example of validating a response
    is_valid = validate_response(questions, 0, "1")
    print(f"Response validation: {'Valid' if is_valid else 'Invalid'}")

    # Example of dumping and loading history
    history_data = dump_history(new_state)
    print(f"Dumped history size: {len(history_data)} bytes")

    # Load the history
    loaded_state = load_history(history_data)
    print(f"Loaded {len(loaded_state.messages)} messages from history")


async def load_and_validate_responses(session, file_content: bytes, input_text: str, axis_id: Optional[int] = None):
    """
    Load chat history, process a new message, and validate responses.

    Args:
        session: SQLAlchemy session
        file_content: Pickled session data
        input_text: User's input text
        axis_id: Optional axis ID filter

    Returns:
        tuple: New file content and response
    """
    # Create repository
    repository = MaturityQuestionRepository(session)

    # Process the interaction
    new_file_content, response = await process_survey_interaction(
        repository,
        input_text,
        file_content=file_content,
        axis_id=axis_id
    )

    return new_file_content, response


if __name__ == "__main__":
    # This would be run from a script that has access to a database session
    # asyncio.run(run_survey_example(session, axis_id=1))
    print("Import this module and use the functions with a database session")
