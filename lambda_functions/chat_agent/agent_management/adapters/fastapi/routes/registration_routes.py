from functools import partial
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.postgres.repositories.registration_repository import RegistrationRepository
from adapters.postgres.config import get_session
from domain.command_handlers.registration_command_handler import get_registration
from domain.command.registration_command import RegistrationResponse
from domain.command.user_command import GetUser
from domain.command.comon_command import Sources, sql


router = APIRouter(prefix="/registration", tags=["agents"])


async def create_registration_handler(
    session: AsyncSession = Depends(get_session)
) -> Callable:
    """
    Create a registration handler with dependency injection.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        Callable: Registration handler function
    """
    repository = RegistrationRepository(session)
    sql_object = sql(registration=repository)
    sources = Sources(sql=sql_object, asistant=None, storage=None)
    return partial(get_registration, sources)


@router.get("/get_user_data", response_model=RegistrationResponse)
async def get_user_data_route(
    command: GetUser,
    handler: Callable = Depends(create_registration_handler)
) -> RegistrationResponse:
    """
    Get user data endpoint.
    
    Args:
        command: User data request command
        handler: Injected registration handler
        
    Returns:
        RegistrationResponse: User registration data
    """
    try:
        return await handler(command)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to get user data: {str(e)}"
        )
