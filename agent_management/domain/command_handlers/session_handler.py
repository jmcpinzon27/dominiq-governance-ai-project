"""Handler for session-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.session_command import (
    CreateSession,
    UpdateSession,
    DeleteSession,
    GetSession,
    SessionResponse,
    ListSessions
)


async def create_session(repository: Callable, command: CreateSession) -> int:
    """Create a new session."""
    return await repository.create(command)


async def update_session(repository: Callable, command: UpdateSession) -> bool:
    """Update an existing session."""
    return await repository.update(command)


async def delete_session(repository: Callable, command: DeleteSession) -> bool:
    """Delete a session."""
    return await repository.delete(command.session_id)


async def get_session(repository: Callable, command: GetSession) -> Optional[SessionResponse]:
    """Retrieve a session by ID, token, or user_id."""
    return await repository.get(command)


async def list_sessions(repository: Callable, active_only: bool = False) -> ListSessions:
    """List all sessions, optionally filtering for active ones only."""
    sessions = await repository.list_all(active_only)
    return ListSessions(sessions=sessions)


async def deactivate_session(repository: Callable, session_id: int) -> bool:
    """Deactivate a session by setting is_active to False and session_end."""
    return await repository.deactivate(session_id)


def create_session_handler(repository: Callable) -> dict:
    """Create a session handler with all methods."""
    return {
        'create_session': partial(create_session, repository),
        'update_session': partial(update_session, repository),
        'delete_session': partial(delete_session, repository),
        'get_session': partial(get_session, repository),
        'list_sessions': partial(list_sessions, repository),
        'deactivate_session': partial(deactivate_session, repository),
    }
