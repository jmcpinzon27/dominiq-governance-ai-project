"""FastAPI routes for project operations."""
from typing import Callable, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.project_command import (
    CreateProject,
    UpdateProject,
    DeleteProject,
    GetProject,
    ProjectResponse,
    ListProjects
)
from domain.command_handlers.project_handler import (
    create_project,
    update_project,
    delete_project,
    get_project,
    list_projects
)
from adapters.postgres.repositories.project_repository import ProjectRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/projects", tags=["projects"])


async def get_project_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for project handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for projects
    """
    repository = ProjectRepository(session)
    return {
        'create_project': lambda cmd: create_project(repository, cmd),
        'update_project': lambda cmd: update_project(repository, cmd),
        'delete_project': lambda cmd: delete_project(repository, cmd),
        'get_project': lambda cmd: get_project(repository, cmd),
        'list_projects': lambda company_id=None: list_projects(repository, company_id)
    }


@router.post("/", response_model=int)
async def create_project_route(
    command: CreateProject,
    handler: dict[str, Callable] = Depends(get_project_handler)
):
    """Create a new project."""
    try:
        return await handler['create_project'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{project_id}", response_model=bool)
async def update_project_route(
    project_id: int,
    command: UpdateProject,
    handler: dict[str, Callable] = Depends(get_project_handler)
):
    """Update an existing project."""
    command.project_id = project_id
    try:
        if not await handler['update_project'](command):
            raise HTTPException(status_code=404, detail="Project not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{project_id}", response_model=bool)
async def delete_project_route(
    project_id: int,
    handler: dict[str, Callable] = Depends(get_project_handler)
):
    """Delete a project."""
    command = DeleteProject(project_id=project_id)
    if not await handler['delete_project'](command):
        raise HTTPException(status_code=404, detail="Project not found")
    return True


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_route(
    project_id: int,
    handler: dict[str, Callable] = Depends(get_project_handler)
):
    """Get a project by ID."""
    command = GetProject(project_id=project_id)
    project = await handler['get_project'](command)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/", response_model=ListProjects)
async def list_projects_route(
    company_id: Optional[int] = Query(None, gt=0),
    handler: dict[str, Callable] = Depends(get_project_handler)
):
    """List all projects, optionally filtered by company_id."""
    return await handler['list_projects'](company_id)
