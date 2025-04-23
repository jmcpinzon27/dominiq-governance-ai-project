"""Repository implementation for project operations."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.project_command import CreateProject, UpdateProject, GetProject, ProjectResponse
from adapters.postgres.models.project import Project


class ProjectRepository:
    """Repository for project operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateProject) -> int:
        """Create a new project."""
        project = Project(
            project_name=command.project_name,
            description=command.description,
            company_id=command.company_id
        )
        self.session.add(project)
        try:
            await self.session.commit()
            await self.session.refresh(project)
            return project.project_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(
                "Project name already exists for this company or invalid company ID")

    async def update(self, command: UpdateProject) -> bool:
        """Update an existing project."""
        stmt = select(Project).where(Project.project_id == command.project_id)
        result = await self.session.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            return False

        project.project_name = command.project_name
        project.description = command.description
        project.company_id = command.company_id

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(
                "Project name already exists for this company or invalid company ID")

    async def delete(self, project_id: int) -> bool:
        """Delete a project."""
        stmt = select(Project).where(Project.project_id == project_id)
        result = await self.session.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            return False

        await self.session.delete(project)
        await self.session.commit()
        return True

    async def get(self, command: GetProject) -> Optional[ProjectResponse]:
        """Get a project by ID, name, or company_id."""
        stmt = select(Project)
        if command.project_id:
            stmt = stmt.where(Project.project_id == command.project_id)
        elif command.project_name and command.company_id:
            stmt = stmt.where(
                Project.project_name == command.project_name,
                Project.company_id == command.company_id
            )
        else:
            return None

        result = await self.session.execute(stmt)
        project = result.scalar_one_or_none()
        return ProjectResponse.model_validate(project) if project else None

    async def list(self, company_id: Optional[int] = None) -> List[ProjectResponse]:
        """List all projects, optionally filtered by company_id."""
        stmt = select(Project)
        if company_id:
            stmt = stmt.where(Project.company_id == company_id)
        result = await self.session.execute(stmt)
        projects = result.scalars().all()
        return [ProjectResponse.model_validate(project) for project in projects]
