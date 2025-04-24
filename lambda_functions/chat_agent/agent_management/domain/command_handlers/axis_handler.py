"""Handler for axis-related commands."""
from typing import Optional, List, Callable
from functools import partial

from domain.command.axis_command import (
    CreateAxis,
    UpdateAxis,
    DeleteAxis,
    GetAxis,
    AxisResponse,
    ListAxes
)


async def create_axis(repository: Callable, command: CreateAxis) -> int:
    """Create a new axis.
    
    Args:
        repository: Axis repository
        command: CreateAxis command
        
    Returns:
        int: ID of the created axis
    """
    return await repository.create(command)


async def update_axis(repository: Callable, command: UpdateAxis) -> bool:
    """Update an existing axis.
    
    Args:
        repository: Axis repository
        command: UpdateAxis command
        
    Returns:
        bool: True if update was successful
    """
    return await repository.update(command)


async def delete_axis(repository: Callable, command: DeleteAxis) -> bool:
    """Delete an axis.
    
    Args:
        repository: Axis repository
        command: DeleteAxis command
        
    Returns:
        bool: True if deletion was successful
    """
    return await repository.delete(command.axis_id)


async def get_axis(repository: Callable, command: GetAxis) -> Optional[AxisResponse]:
    """Get an axis by ID.
    
    Args:
        repository: Axis repository
        command: GetAxis command
        
    Returns:
        Optional[AxisResponse]: Axis data if found, None otherwise
    """
    return await repository.get_by_id(command.axis_id)


async def list_axes(repository: Callable) -> ListAxes:
    """List all axes.
    
    Args:
        repository: Axis repository
        
    Returns:
        ListAxes: List of all axes
    """
    axes = await repository.get_all()
    return ListAxes(axes=axes)


def create_axis_handler(repository: Callable) -> dict:
    """Create a dictionary of axis handler functions.
    
    Args:
        repository: Axis repository
        
    Returns:
        dict: Dictionary of handler functions
    """
    return {
        'create_axis': partial(create_axis, repository),
        'update_axis': partial(update_axis, repository),
        'delete_axis': partial(delete_axis, repository),
        'get_axis': partial(get_axis, repository),
        'list_axes': partial(list_axes, repository),
    }
