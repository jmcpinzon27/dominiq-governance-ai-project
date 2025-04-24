"""
LangChain adapter for SAIA.ai API.

This module provides a functional implementation for interacting with the SAIA.ai API,
specifically designed for survey applications using maturity questions.
"""
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from functools import lru_cache
import json

from pydantic import BaseModel, Field, field_validator
from langchain.prompts import ChatPromptTemplate
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from domain.command.maturity_question_command import (
    Question,
    QuestionOption,
    SurveyResponse,
    SurveyState,
    ChatMessage,
    ChatResponse
)

# API Configuration
SAIA_CONFIG = {
    "base_url": "https://api.saia.ai",
    "assistant_id": "ba4df829-9c61-4a7a-8f60-aa911a6d0a54",
    "headers": {
        "Authorization": "Bearer default_QJ6z12CWdeLnW3uKOag7xUUkzmwOC8vQk161eAJyV4NT4ozBkZyruWW9XdJqxuNKqjTVLcnS3EWt7QF9qff_C0t0-JkoevWcaOmVpzwgq6E968Dg6HfDZWEWWorsaO4j_fgC_gV3GNM3_qXgDuKr7jUbeE7xu8va9BeTlVA-Lb4=",
        "Content-Type": "application/json"
    },
    "timeout": 10,
    "saia-conversation-id": "user1",
    "default_user": "user1"
}


def create_http_session() -> requests.Session:
    """
    Create and configure a reusable HTTP session with retry capability.
    
    Returns:
        requests.Session: Configured session
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT"]
    )
    session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    return session

async def call_saia_api(
    user_id: str = SAIA_CONFIG["default_user"],
    model_name: str = "saia:assistant:[DominiQ]Maturity",
    revision: int = 1,
    messages: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    Call the SAIA API with the given prompt.
    """
    session = create_http_session()

    try:
        response = session.post(
            f'{SAIA_CONFIG["base_url"]}/chat/completions',
            headers={**SAIA_CONFIG["headers"], "saia-conversation-id": user_id},
            json={
                "model": model_name,
                "revision": revision,
                "messages": messages
            },
            timeout=SAIA_CONFIG["timeout"]
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"API call error: {e}")
        return json.dumps({
            "question_number": 0,
            "total_questions": 0,
            "current_question": "",
            "assistant_message": "I apologize, but I couldn't generate a response at this time.",
            "next_action": "ERROR"
        })

class SurveyPromptResponse(BaseModel):
    """Structured response from LLM"""
    last_question_id: int | None = None
    last_question_option: Optional[str] = None
    question_number: int | None = None
    total_questions: int| None = None
    assistant_message: str
    next_action: str = Field(default="CONTINUE")  # CONTINUE, COMPLETE, ERROR
    
    @field_validator('next_action')
    def validate_next_action(cls, v):
        allowed = {'CONTINUE', 'COMPLETE', 'ERROR'}
        if v not in allowed:
            raise ValueError(f'next_action must be one of {allowed}')
        return v

def create_survey_prompt(questions: List[Question]) -> str:
    """
    Create the survey prompt template with structured response format.
    """
    questions_str = json.dumps([q.model_dump() for q in questions])
    return f"""
    You are a Globant survey assistant. Introduce yourself and ask questions one by one.

    QUESTIONS = {questions_str}

    Guidelines:
    - Present one question at a time from QUESTIONS
    - Show numbered options (1 being lowest)
    - Track progress ({len(questions)} total questions)
    - Be conversational and friendly
    - Store responses for analysis

    IMPORTANT: Always respond in the following JSON format:
    {{
        "last_question_id": "<last question id>",
        "last_question_option": "<last question option text>",
        "question_number": <current question number>,
        "total_questions": {len(questions)},
        "assistant_message": "<your conversational response>",
        "next_action": "<CONTINUE|COMPLETE|ERROR>"
    }}
    """

async def initialize_survey(
    questions: List[Question],
    user_id: str = SAIA_CONFIG["default_user"],
    revision: int = 1,
    temperature: float = 0.0
) -> SurveyState:
    """
    Initialize a new survey session by creating a new assistant.
    
    Args:
        questions: Survey questions
        user_id: User identifier
        revision: Model revision
        temperature: Temperature parameter
    
    Returns:
        SurveyState: Initial survey state
    """
    prompt = create_survey_prompt(questions)
    
    try:
        session = create_http_session()
        
        json = {
            "action": "save", #savePublishNewRevision. Save updates the specified revision ID
            "revisionId": revision,
            "prompt": prompt,
            "llmSettings":{
            "modelName":"gpt-4o-mini",
            "temperature":temperature
            }
        }
        response = session.put(
            f'{SAIA_CONFIG["base_url"]}/v1/assistant/{SAIA_CONFIG["assistant_id"]}',
            headers=SAIA_CONFIG["headers"],
            json=json,
            timeout=SAIA_CONFIG["timeout"]
        )
        response.raise_for_status()
        
        return SurveyState(
            user_id=user_id,
            questions=questions
        )
    except Exception as e:
        print(f"Initialization error: {e}")
        return SurveyState(user_id=user_id, questions=questions)

async def process_response(
    state: SurveyState,
    response_text: str
) -> Tuple[SurveyState, Optional[SurveyPromptResponse]]:
    """
    Process a user response and update survey state.
    """
    current_question = state.questions[state.current_question_idx]
    
    try:
        # Update state and get AI response
        message = [{"role": "user", "content": response_text}]
        new_messages = state.messages + message
        ai_response = await call_saia_api(state.user_id, messages=new_messages)
        
        try:
            # Parse the JSON response into our Pydantic model
            structured_response = SurveyPromptResponse.model_validate_json(ai_response)
            
            # Update state with formatted message
            assistant_message = {
                "role": "assistant",
                "content": structured_response.assistant_message
            }
            
            new_state = SurveyState(
                user_id=state.user_id,
                messages=[*new_messages, assistant_message],
                questions=state.questions,
                current_question_idx=(
                    min(state.current_question_idx + 1, len(state.questions) - 1)
                    if structured_response.next_action == "CONTINUE"
                    else state.current_question_idx
                ),
                responses={**state.responses, structured_response.last_question_id: structured_response.last_question_option}
                        if structured_response.last_question_id else state.responses
            )
            
            return new_state, assistant_message
            
        except ValueError as json_error:
            # Handle case where LLM response isn't in expected format
            error_response = SurveyPromptResponse(
                question_number=state.current_question_idx + 1,
                total_questions=len(state.questions),
                current_question=current_question,
                assistant_message="Error processing response format",
                next_action="ERROR"
            )
            return state, error_response
        
    except ValueError as e:
        return state, None

def save_survey_state(state: SurveyState) -> bytes:
    """
    Serialize survey state.
    
    Args:
        state: Survey state to save
    
    Returns:
        bytes: Serialized state
    """
    return json.dumps(state.model_dump()).encode()

def load_survey_state(data: bytes) -> Optional[SurveyState]:
    """
    Deserialize survey state.
    
    Args:
        data: Serialized state data
    
    Returns:
        Optional[SurveyState]: Loaded state or None if invalid
    """
    try:
        state_dict = json.loads(data.decode())
        return SurveyState(**state_dict)
    except Exception as e:
        print(f"State loading error: {e}")
        return None
