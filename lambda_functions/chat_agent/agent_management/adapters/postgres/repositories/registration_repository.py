"""Repository implementation for project operations."""
from typing import Optional, List
from sqlalchemy import select, and_, join, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from adapters.postgres.models.user import User
from adapters.postgres.models.project import Project
from adapters.postgres.models.domain import Domain
from adapters.postgres.models.subdomain import Subdomain
from adapters.postgres.models.company import Company
from domain.command.user_command import GetUser
from domain.command.registration_command import RegistrationResponse


class RegistrationRepository:

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session


    async def get(self, command: GetUser) -> Optional[RegistrationResponse]:
        # TODO: responsible is not the use
        # TODO: los subdominios, dominios retornan muchos
        
        # stmt = (
        #     select(
        #         User.email,
        #         User.user_id,
        #         User.user_name.label('responsible'),
        #         Subdomain.subdomain_name.label('subdomain'),
        #         Domain.domain_name.label('domain'),
        #         Industry.project_name.label('industry')
        #     )
        #         .join(Company, User.company_id == Company.company_id)
        #         .join(Domain, Domain.company_id == Company.company_id)
        #         .join(Subdomain, Subdomain.domain_id == Domain.domain_id)
        #         .outerjoin(Project, Project.company_id == Company.company_id)                
        #         .where(User.email == command.email)
        # )
        stmt = (
            select(
                User.email,
                User.user_id,
                User.user_name.label('responsible')
            )
            .where(User.email.ilike(f"%{command.email}%"))
            .order_by(User.user_name)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return RegistrationResponse.model_validate(result.fetchone()) if result else None
