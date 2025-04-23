from domain.command.comon_command import Sources
from domain.command.registration_command import GetUser


async def get_registration(sources: Sources, data: GetUser):
    return await sources.sql.registration.get(data)