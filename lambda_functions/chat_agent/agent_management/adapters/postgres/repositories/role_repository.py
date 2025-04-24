"""Repository implementation for role operations."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.role_command import CreateRole, UpdateRole, GetRole, RoleResponse
from adapters.postgres.models.role import Role


class RoleRepository:
    """Repository for role operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateRole) -> int:
        """Create a new role."""
        role = Role(
            role_name=command.role_name,
            description=command.description
        )
        self.session.add(role)
        try:
            await self.session.commit()
            await self.session.refresh(role)
            return role.role_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Role name already exists")

    async def update(self, command: UpdateRole) -> bool:
        """Update an existing role."""
        stmt = select(Role).where(Role.role_id == command.role_id)
        result = await self.session.execute(stmt)
        role = result.scalar_one_or_none()

        if not role:
            return False

        role.role_name = command.role_name
        role.description = command.description

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Role name already exists")

    async def delete(self, role_id: int) -> bool:
        """Delete a role."""
        stmt = select(Role).where(Role.role_id == role_id)
        result = await self.session.execute(stmt)
        role = result.scalar_one_or_none()

        if not role:
            return False

        await self.session.delete(role)
        await self.session.commit()
        return True

    async def get(self, command: GetRole) -> Optional[RoleResponse]:
        """Get a role by ID or name."""
        stmt = select(Role)
        if command.role_id:
            stmt = stmt.where(Role.role_id == command.role_id)
        elif command.role_name:
            stmt = stmt.where(Role.role_name == command.role_name)
        else:
            return None

        result = await self.session.execute(stmt)
        role = result.scalar_one_or_none()
        return RoleResponse.model_validate(role) if role else None

    async def list(self) -> List[RoleResponse]:
        """List all roles."""
        stmt = select(Role)
        result = await self.session.execute(stmt)
        roles = result.scalars().all()
        return [RoleResponse.model_validate(role) for role in roles]
