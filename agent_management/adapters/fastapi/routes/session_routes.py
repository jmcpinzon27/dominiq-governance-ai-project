"""FastAPI routes for session operations."""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.session_command import (
    CreateSession,
    UpdateSession,
    DeleteSession,
    GetSession,
    SessionResponse,
    ListSessions
)
from domain.command_handlers.session_handler import (
    create_session,
    update_session,
    delete_session,
    get_session,
    list_sessions,
    deactivate_session
)
from adapters.postgres.repositories.session_repository import SessionRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/sessions", tags=["sessions"])


async def get_session_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for session handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for sessions
    """
    repository = SessionRepository(session)
    return {
        'create_session': lambda cmd: create_session(repository, cmd),
        'update_session': lambda cmd: update_session(repository, cmd),
        'delete_session': lambda cmd: delete_session(repository, cmd),
        'get_session': lambda cmd: get_session(repository, cmd),
        'list_sessions': lambda active_only: list_sessions(repository, active_only),
        'deactivate_session': lambda session_id: deactivate_session(repository, session_id)
    }


@router.post("/", response_model=int)
async def create_session_route(
    command: CreateSession,
    handler: dict[str, Callable] = Depends(get_session_handler)
):
    """Create a new session."""
    try:
        return await handler['create_session'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{session_id}", response_model=bool)
async def update_session_route(
    session_id: int,
    command: UpdateSession,
    handler: dict[str, Callable] = Depends(get_session_handler)
):
    """Update an existing session."""
    command.session_id = session_id
    try:
        if not await handler['update_session'](command):
            raise HTTPException(status_code=404, detail="Session not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{session_id}", response_model=bool)
async def delete_session_route(
    session_id: int,
    handler: dict[str, Callable] = Depends(get_session_handler)
):
    """Delete a session."""
    command = DeleteSession(session_id=session_id)
    if not await handler['delete_session'](command):
        raise HTTPException(status_code=404, detail="Session not found")
    return True


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session_route(
    session_id: int,
    handler: dict[str, Callable] = Depends(get_session_handler)
):
    """Get a session by ID."""
    command = GetSession(session_id=session_id)
    session = await handler['get_session'](command)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/", response_model=ListSessions)
async def list_sessions_route(
    active_only: bool = Query(False, description="Filter for active sessions only"),
    handler: dict[str, Callable] = Depends(get_session_handler)
):
    """List all sessions."""
    return await handler['list_sessions'](active_only)


@router.post("/{session_id}/deactivate", response_model=bool)
async def deactivate_session_route(
    session_id: int,
    handler: dict[str, Callable] = Depends(get_session_handler)
):
    """Deactivate a session."""
    if not await handler['deactivate_session'](session_id):
        raise HTTPException(status_code=404, detail="Session not found or already inactive")
    return True
