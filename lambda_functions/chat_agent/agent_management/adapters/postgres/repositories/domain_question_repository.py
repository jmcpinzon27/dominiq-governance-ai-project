"""Repository implementation for domain question operations."""
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.domain_question_command import (
    CreateDomainQuestion,
    UpdateDomainQuestion,
    GetDomainQuestion,
    DomainQuestionResponse
)
from adapters.postgres.models.domain_question import DomainQuestion


class DomainQuestionRepository:
    """Repository for domain question operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateDomainQuestion) -> int:
        """Create a new domain question."""
        domain_question = DomainQuestion(
            domain_id=command.domain_id,
            industry_id=command.industry_id,
            question_text=command.question_text,
            question_type=command.question_type,
            category=command.category
        )
        self.session.add(domain_question)
        await self.session.commit()
        await self.session.refresh(domain_question)
        return domain_question.domain_question_id

    async def update(self, command: UpdateDomainQuestion) -> bool:
        """Update an existing domain question."""
        stmt = select(DomainQuestion).where(
            DomainQuestion.domain_question_id == command.domain_question_id
        )
        result = await self.session.execute(stmt)
        domain_question = result.scalar_one_or_none()

        if not domain_question:
            return False

        domain_question.domain_id = command.domain_id
        domain_question.industry_id = command.industry_id
        domain_question.question_text = command.question_text
        domain_question.question_type = command.question_type
        domain_question.category = command.category

        await self.session.commit()
        return True

    async def delete(self, domain_question_id: int) -> bool:
        """Delete a domain question."""
        stmt = select(DomainQuestion).where(
            DomainQuestion.domain_question_id == domain_question_id
        )
        result = await self.session.execute(stmt)
        domain_question = result.scalar_one_or_none()

        if not domain_question:
            return False

        await self.session.delete(domain_question)
        await self.session.commit()
        return True

    async def get(self, command: GetDomainQuestion) -> Optional[DomainQuestionResponse]:
        """Get a domain question by ID or filters."""
        stmt = select(DomainQuestion)

        conditions = []
        if command.domain_question_id:
            conditions.append(DomainQuestion.domain_question_id ==
                              command.domain_question_id)
        if command.domain_id:
            conditions.append(DomainQuestion.domain_id == command.domain_id)
        if command.industry_id:
            conditions.append(DomainQuestion.industry_id == command.industry_id)
        if command.category:
            conditions.append(DomainQuestion.category == command.category)
        if command.question_type:
            conditions.append(DomainQuestion.question_type ==
                              command.question_type)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.session.execute(stmt)
        domain_question = result.scalar_one_or_none()
        return DomainQuestionResponse.model_validate(domain_question) if domain_question else None

    async def list_all(
        self,
        domain_id: Optional[int] = None,
        industry_id: Optional[int] = None,
        category: Optional[str] = None,
        question_type: Optional[str] = None
    ) -> List[DomainQuestionResponse]:
        """List all domain questions, optionally filtered."""
        stmt = select(DomainQuestion)

        if domain_id:
            stmt = stmt.where(DomainQuestion.domain_id == domain_id)
        if industry_id:
            stmt = stmt.where(DomainQuestion.industry_id == industry_id)
        if category:
            stmt = stmt.where(DomainQuestion.category == category)
        if question_type:
            stmt = stmt.where(DomainQuestion.question_type == question_type)

        result = await self.session.execute(stmt)
        domain_questions = result.scalars().all()
        return [DomainQuestionResponse.model_validate(q) for q in domain_questions]
