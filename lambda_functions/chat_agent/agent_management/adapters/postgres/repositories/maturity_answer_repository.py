"""Repository implementation for maturity answer operations."""
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.maturity_answer_command import (
    CreateMaturityAnswer,
    UpdateMaturityAnswer,
    GetMaturityAnswer,
    MaturityAnswerResponse
)
from adapters.postgres.models.maturity_answer import MaturityAnswer


class MaturityAnswerRepository:
    """Repository for maturity answer operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateMaturityAnswer) -> int:
        """Create a new maturity answer.
        
        Args:
            command: CreateMaturityAnswer command
            
        Returns:
            int: ID of the created maturity answer
            
        Raises:
            ValueError: If maturity answer already exists for this session and question
        """
        try:
            maturity_answer = MaturityAnswer(
                session_id=command.session_id,
                maturity_question_id=command.maturity_question_id,
                answer_text=command.answer_text,
                answered_at=command.answered_at
            )
            self.session.add(maturity_answer)
            await self.session.commit()
            await self.session.refresh(maturity_answer)
            return maturity_answer.maturity_answer_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(
                "Maturity answer already exists for this session and question")

    async def update(self, command: UpdateMaturityAnswer) -> bool:
        """Update an existing maturity answer.
        
        Args:
            command: UpdateMaturityAnswer command
            
        Returns:
            bool: True if update was successful
            
        Raises:
            ValueError: If maturity answer already exists for this session and question
        """
        stmt = select(MaturityAnswer).where(MaturityAnswer.maturity_answer_id == command.maturity_answer_id)
        result = await self.session.execute(stmt)
        maturity_answer = result.scalar_one_or_none()

        if not maturity_answer:
            return False

        maturity_answer.session_id = command.session_id
        maturity_answer.maturity_question_id = command.maturity_question_id
        maturity_answer.answer_text = command.answer_text
        maturity_answer.answered_at = command.answered_at

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(
                "Maturity answer already exists for this session and question")

    async def delete(self, maturity_answer_id: int) -> bool:
        """Delete a maturity answer.
        
        Args:
            maturity_answer_id: ID of the maturity answer to delete
            
        Returns:
            bool: True if deletion was successful
        """
        stmt = select(MaturityAnswer).where(MaturityAnswer.maturity_answer_id == maturity_answer_id)
        result = await self.session.execute(stmt)
        maturity_answer = result.scalar_one_or_none()

        if not maturity_answer:
            return False

        await self.session.delete(maturity_answer)
        await self.session.commit()
        return True

    async def get(self, command: GetMaturityAnswer) -> Optional[MaturityAnswerResponse]:
        """Get a maturity answer by ID or filters.
        
        Args:
            command: GetMaturityAnswer command
            
        Returns:
            Optional[MaturityAnswerResponse]: Maturity answer data if found, None otherwise
        """
        stmt = select(MaturityAnswer)

        conditions = []
        if command.maturity_answer_id:
            conditions.append(MaturityAnswer.maturity_answer_id == command.maturity_answer_id)
        if command.session_id:
            conditions.append(MaturityAnswer.session_id == command.session_id)
        if command.maturity_question_id:
            conditions.append(MaturityAnswer.maturity_question_id == command.maturity_question_id)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.session.execute(stmt)
        maturity_answer = result.scalar_one_or_none()
        return MaturityAnswerResponse.model_validate(maturity_answer) if maturity_answer else None

    async def list_all(
        self,
        session_id: Optional[int] = None,
        maturity_question_id: Optional[int] = None
    ) -> List[MaturityAnswerResponse]:
        """List all maturity answers, optionally filtered.
        
        Args:
            session_id: Optional session ID filter
            maturity_question_id: Optional maturity question ID filter
            
        Returns:
            List[MaturityAnswerResponse]: List of maturity answers
        """
        stmt = select(MaturityAnswer)

        if session_id:
            stmt = stmt.where(MaturityAnswer.session_id == session_id)
        if maturity_question_id:
            stmt = stmt.where(MaturityAnswer.maturity_question_id == maturity_question_id)

        result = await self.session.execute(stmt)
        maturity_answers = result.scalars().all()
        return [MaturityAnswerResponse.model_validate(a) for a in maturity_answers]
