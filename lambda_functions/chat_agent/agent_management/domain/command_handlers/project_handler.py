"""Handler for project-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.project_command import (
    CreateProject,
    UpdateProject,
    DeleteProject,
    GetProject,
    ProjectResponse,
    ListProjects
)


async def create_project(repository: Callable, command: CreateProject) -> int:
    """Create a new project."""
    return await repository.create(command)


async def update_project(repository: Callable, command: UpdateProject) -> bool:
    """Update an existing project."""
    return await repository.update(command)


async def delete_project(repository: Callable, command: DeleteProject) -> bool:
    """Delete a project."""
    return await repository.delete(command.project_id)


async def get_project(repository: Callable, command: GetProject) -> Optional[ProjectResponse]:
    """Retrieve a project by ID, name, or company_id."""
    return await repository.get(command)


async def list_projects(repository: Callable, company_id: Optional[int] = None) -> ListProjects:
    """List all projects, optionally filtered by company_id."""
    projects = await repository.list(company_id)
    return ListProjects(projects=projects)


def create_project_handler(repository: Callable) -> dict:
    """Create a dictionary of project-related functions with repository dependency."""
    return {
        'create_project': partial(create_project, repository),
        'update_project': partial(update_project, repository),
        'delete_project': partial(delete_project, repository),
        'get_project': partial(get_project, repository),
        'list_projects': partial(list_projects, repository)
    }
