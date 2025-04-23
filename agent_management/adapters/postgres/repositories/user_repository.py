"""Repository implementation for user operations."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.user_command import CreateUser, UpdateUser, GetUser, UserResponse
from adapters.postgres.models.user import User


class UserRepository:
    """Repository for user operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateUser) -> int:
        """Create a new user."""
        user = User(
            user_name=command.user_name,
            email=command.email,
            role_id=command.role_id,
            company_id=command.company_id
        )
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user.user_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Email already exists or invalid role/company ID")

    async def update(self, command: UpdateUser) -> bool:
        """Update an existing user."""
        stmt = select(User).where(User.user_id == command.user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return False

        user.user_name = command.user_name
        user.email = command.email
        user.role_id = command.role_id
        user.company_id = command.company_id

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Email already exists or invalid role/company ID")

    async def delete(self, user_id: int) -> bool:
        """Delete a user."""
        stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True

    async def get(self, command: GetUser) -> Optional[UserResponse]:
        """Get a user by ID or email."""
        stmt = select(User)
        if command.user_id:
            stmt = stmt.where(User.user_id == command.user_id)
        elif command.email:
            stmt = stmt.where(User.email == command.email)
        else:
            return None

        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserResponse.model_validate(user) if user else None

    async def list(self) -> List[UserResponse]:
        """List all users."""
        stmt = select(User)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return [UserResponse.model_validate(user) for user in users]
