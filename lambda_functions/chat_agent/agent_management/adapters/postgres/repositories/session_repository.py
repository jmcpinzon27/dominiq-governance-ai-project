"""Repository implementation for session operations."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.session_command import CreateSession, UpdateSession, GetSession, SessionResponse
from adapters.postgres.models.session import Session


class SessionRepository:
    """Repository for session operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateSession) -> int:
        """Create a new session."""
        session = Session(
            user_id=command.user_id,
            session_token=command.session_token,
            is_active=command.is_active,
            session_start=command.session_start,
            session_end=command.session_end
        )
        self.session.add(session)
        try:
            await self.session.commit()
            await self.session.refresh(session)
            return session.session_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Session token already exists or invalid user_id")

    async def update(self, command: UpdateSession) -> bool:
        """Update an existing session."""
        stmt = select(Session).where(Session.session_id == command.session_id)
        result = await self.session.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            return False

        session.user_id = command.user_id
        session.session_token = command.session_token
        session.is_active = command.is_active
        session.session_end = command.session_end

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Session token already exists or invalid user_id")

    async def delete(self, session_id: int) -> bool:
        """Delete a session."""
        stmt = select(Session).where(Session.session_id == session_id)
        result = await self.session.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            return False

        await self.session.delete(session)
        await self.session.commit()
        return True

    async def get(self, command: GetSession) -> Optional[SessionResponse]:
        """Get a session by ID, token, or user_id."""
        stmt = select(Session)
        if command.session_id:
            stmt = stmt.where(Session.session_id == command.session_id)
        elif command.session_token:
            stmt = stmt.where(Session.session_token == command.session_token)
        elif command.user_id:
            stmt = stmt.where(Session.user_id == command.user_id)
        else:
            return None

        result = await self.session.execute(stmt)
        session = result.scalar_one_or_none()
        return SessionResponse.model_validate(session) if session else None

    async def list_all(self, active_only: bool = False) -> List[SessionResponse]:
        """List all sessions, optionally filtering for active ones only."""
        stmt = select(Session)
        if active_only:
            stmt = stmt.where(Session.is_active == True)
        result = await self.session.execute(stmt)
        sessions = result.scalars().all()
        return [SessionResponse.model_validate(session) for session in sessions]

    async def deactivate(self, session_id: int) -> bool:
        """Deactivate a session."""
        stmt = select(Session).where(
            and_(Session.session_id == session_id, Session.is_active == True)
        )
        result = await self.session.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            return False

        session.is_active = False
        session.session_end = datetime.utcnow()
        await self.session.commit()
        return True
