"""
Tests for SAIA.ai LangChain adapter.

This module provides tests for the SAIA.ai LangChain adapter,
specifically for survey applications with maturity questions.
"""
import pytest
import pickle
from unittest.mock import MagicMock, patch
from datetime import datetime

from adapters.saia.saia_adapter import (
    SaiaLLM,
    SaiaSurveyManager,
    SaiaSurveyChain,
    Question,
    QuestionOption,
    ChatMessage,
    ChatResponse
)


@pytest.fixture
def mock_session():
    """Create a mock session."""
    session = MagicMock()
    return session


@pytest.fixture
def mock_repository(mock_session):
    """Create a mock repository."""
    repository = MagicMock()
    repository.session = mock_session

    # Mock the get_questions_with_response method
    async def mock_get_questions(*args, **kwargs):
        # Create mock document objects
        class MockDocument:
            def __init__(self, page_content, metadata):
                self.page_content = page_content
                self.metadata = metadata

        return [
            MockDocument(
                page_content={
                    'question_text': 'What is your data maturity level?',
                    'options': 'id:1, text:Low\nid:2, text:Medium\nid:3, text:High'
                },
                metadata={
                    'category': 'Data Maturity',
                    'subset': 'General'
                }
            ),
            MockDocument(
                page_content={
                    'question_text': 'How do you manage data quality?',
                    'options': 'id:4, text:Manual processes\nid:5, text:Automated tools\nid:6, text:AI-driven'
                },
                metadata={
                    'category': 'Data Quality',
                    'subset': 'Management'
                }
            )
        ]

    repository.get_questions_with_response = mock_get_questions
    return repository


@pytest.fixture
def mock_llm():
    """Create a mock LLM."""
    with patch('adapters.langchain.saia_adapter.SaiaLLM._call') as mock_call:
        mock_call.return_value = "This is a mock response from the LLM."
        llm = SaiaLLM()
        yield llm


@pytest.mark.asyncio
async def test_load_questions_from_repository(mock_repository):
    """Test loading questions from the repository."""
    # Create a survey manager
    manager = SaiaSurveyManager()

    # Load questions
    questions = await manager.load_questions_from_repository(mock_repository)

    # Verify questions were loaded correctly
    assert len(questions) == 2
    assert questions[0].question_text == 'What is your data maturity level?'
    assert len(questions[0].options) == 3
    assert questions[0].options[0].id == 1
    assert questions[0].options[0].text == 'Low'
    assert questions[0].category == 'Data Maturity'
    assert questions[0].subset == 'General'


def test_process_message(mock_llm):
    """Test processing a message."""
    # Create a survey manager with the mock LLM
    manager = SaiaSurveyManager()
    manager.llm = mock_llm

    # Process a message
    response = manager.process_message("Hello, I'm ready for the survey")

    # Verify response
    assert isinstance(response, ChatResponse)
    assert response.messages.role == "assistant"
    assert response.messages.content == "This is a mock response from the LLM."
    assert len(manager.messages) == 2
    assert manager.messages[0]["role"] == "user"
    assert manager.messages[0]["content"] == "Hello, I'm ready for the survey"
    assert manager.messages[1]["role"] == "assistant"
    assert manager.messages[1]["content"] == "This is a mock response from the LLM."


def test_validate_response():
    """Test validating a response."""
    # Create a survey manager
    manager = SaiaSurveyManager()

    # Add a question with options
    manager.questions = [
        Question(
            question_text="What is your data maturity level?",
            options=[
                QuestionOption(id=1, text="Low"),
                QuestionOption(id=2, text="Medium"),
                QuestionOption(id=3, text="High")
            ]
        )
    ]

    # Test valid responses
    assert manager.validate_response(0, "1") is True
    assert manager.validate_response(0, "2") is True
    assert manager.validate_response(0, "3") is True
    assert manager.validate_response(0, "Low") is True

    # Test invalid responses
    assert manager.validate_response(0, "4") is False
    assert manager.validate_response(0, "Invalid") is False
    assert manager.validate_response(1, "1") is False  # Invalid question ID


def test_dump_and_load_history():
    """Test dumping and loading history."""
    # Create a survey manager
    manager = SaiaSurveyManager()

    # Add messages and questions
    manager.messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    manager.questions = [
        Question(
            question_text="What is your data maturity level?",
            options=[
                QuestionOption(id=1, text="Low"),
                QuestionOption(id=2, text="Medium"),
                QuestionOption(id=3, text="High")
            ]
        )
    ]

    # Dump history
    history_data = manager.dump_history()

    # Create a new manager
    new_manager = SaiaSurveyManager()

    # Load history
    assert new_manager.load_history(history_data) is True

    # Verify loaded data
    assert len(new_manager.messages) == 2
    assert new_manager.messages[0]["role"] == "user"
    assert new_manager.messages[0]["content"] == "Hello"
    assert new_manager.messages[1]["role"] == "assistant"
    assert new_manager.messages[1]["content"] == "Hi there!"


@pytest.mark.asyncio
async def test_create_survey_chain(mock_repository, mock_llm):
    """Test creating a survey chain."""
    with patch('adapters.langchain.saia_adapter.create_survey_chain') as mock_create_chain:
        # Setup the mock
        mock_chain = SaiaSurveyChain()
        mock_chain.manager = SaiaSurveyManager()
        mock_chain.manager.questions = [
            Question(
                question_text="What is your data maturity level?",
                options=[
                    QuestionOption(id=1, text="Low"),
                    QuestionOption(id=2, text="Medium"),
                    QuestionOption(id=3, text="High")
                ]
            )
        ]
        mock_create_chain.return_value = mock_chain

        # Create a survey chain
        from adapters.saia.saia_adapter import create_survey_chain
        chain = await create_survey_chain(mock_repository)

        # Verify chain was created correctly
        assert isinstance(chain, SaiaSurveyChain)
        assert len(chain.manager.questions) == 1
        assert mock_create_chain.called
