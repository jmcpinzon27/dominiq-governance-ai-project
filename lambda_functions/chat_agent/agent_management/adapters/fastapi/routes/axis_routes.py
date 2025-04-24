"""FastAPI routes for axis operations."""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.axis_command import (
    CreateAxis,
    UpdateAxis,
    DeleteAxis,
    GetAxis,
    AxisResponse,
    ListAxes
)
from domain.command_handlers.axis_handler import (
    create_axis,
    update_axis,
    delete_axis,
    get_axis,
    list_axes
)
from adapters.postgres.repositories.axis_repository import AxisRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/axes", tags=["axes"])


async def get_axis_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for axis handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for axes
    """
    repository = AxisRepository(session)
    return {
        'create_axis': lambda cmd: create_axis(repository, cmd),
        'update_axis': lambda cmd: update_axis(repository, cmd),
        'delete_axis': lambda cmd: delete_axis(repository, cmd),
        'get_axis': lambda cmd: get_axis(repository, cmd),
        'list_axes': lambda: list_axes(repository)
    }


@router.post("/", response_model=int, status_code=201)
async def create_axis_endpoint(
    command: CreateAxis,
    handler: dict[str, Callable] = Depends(get_axis_handler)
):
    """
    Create a new axis.
    
    Args:
        command: CreateAxis command with axis details
        handler: Axis handler functions
        
    Returns:
        int: ID of the created axis
        
    Raises:
        HTTPException: If axis name already exists
    """
    try:
        return await handler['create_axis'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{axis_id}", response_model=bool)
async def update_axis_endpoint(
    axis_id: int,
    command: UpdateAxis,
    handler: dict[str, Callable] = Depends(get_axis_handler)
):
    """
    Update an existing axis.
    
    Args:
        axis_id: ID of the axis to update
        command: UpdateAxis command with updated axis details
        handler: Axis handler functions
        
    Returns:
        bool: True if update was successful
        
    Raises:
        HTTPException: If axis not found or name already exists
    """
    command.axis_id = axis_id
    try:
        result = await handler['update_axis'](command)
        if not result:
            raise HTTPException(status_code=404, detail="Axis not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{axis_id}", response_model=bool)
async def delete_axis_endpoint(
    axis_id: int,
    handler: dict[str, Callable] = Depends(get_axis_handler)
):
    """
    Delete an axis.
    
    Args:
        axis_id: ID of the axis to delete
        handler: Axis handler functions
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If axis not found
    """
    result = await handler['delete_axis'](DeleteAxis(axis_id=axis_id))
    if not result:
        raise HTTPException(status_code=404, detail="Axis not found")
    return result


@router.get("/{axis_id}", response_model=AxisResponse)
async def get_axis_endpoint(
    axis_id: int,
    handler: dict[str, Callable] = Depends(get_axis_handler)
):
    """
    Get an axis by ID.
    
    Args:
        axis_id: ID of the axis to get
        handler: Axis handler functions
        
    Returns:
        AxisResponse: Axis data
        
    Raises:
        HTTPException: If axis not found
    """
    result = await handler['get_axis'](GetAxis(axis_id=axis_id))
    if not result:
        raise HTTPException(status_code=404, detail="Axis not found")
    return result


@router.get("/", response_model=ListAxes)
async def list_axes_endpoint(
    handler: dict[str, Callable] = Depends(get_axis_handler)
):
    """
    List all axes.
    
    Args:
        handler: Axis handler functions
        
    Returns:
        ListAxes: List of all axes
    """
    return await handler['list_axes']()
