from typing import Optional, List

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.postgres.config import DatabaseSettings
from adapters.postgres.models.maturity_question import MaturityQuestion
from adapters.postgres.models.maturity_agent_response import MaturityAgentResponse
from domain.command.maturity_question_command import (
    CreateMaturityQuestion,
    UpdateMaturityQuestion,
    GetMaturityQuestion,
    MaturityQuestionResponse,
    Question,
    QuestionOption
)


class MaturityQuestionRepository:
    """Repository for maturity question operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateMaturityQuestion) -> int:
        """Create a new maturity question.

        Args:
            command: CreateMaturityQuestion command

        Returns:
            int: ID of the created maturity question

        Raises:
            ValueError: If validation fails
        """
        maturity_question = MaturityQuestion(
            question_text=command.question_text,
            question_type=command.question_type,
            question_order=command.question_order,
            category=command.category,
            axis_id=command.axis_id,
            industry_id=command.industry_id
        )
        self.session.add(maturity_question)
        try:
            await self.session.commit()
            await self.session.refresh(maturity_question)
            return maturity_question.maturity_question_id
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(f"Failed to create maturity question: {str(e)}")

    async def update(self, command: UpdateMaturityQuestion) -> bool:
        """Update an existing maturity question.

        Args:
            command: UpdateMaturityQuestion command

        Returns:
            bool: True if update was successful

        Raises:
            ValueError: If validation fails
        """
        stmt = select(MaturityQuestion).where(
            MaturityQuestion.maturity_question_id == command.maturity_question_id)
        result = await self.session.execute(stmt)
        maturity_question = result.scalar_one_or_none()

        if not maturity_question:
            return False

        maturity_question.question_text = command.question_text
        maturity_question.question_type = command.question_type
        maturity_question.question_order = command.question_order
        maturity_question.category = command.category
        maturity_question.axis_id = command.axis_id
        maturity_question.industry_id = command.industry_id

        try:
            await self.session.commit()
            return True
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(f"Failed to update maturity question: {str(e)}")

    async def delete(self, maturity_question_id: int) -> bool:
        """Delete a maturity question.

        Args:
            maturity_question_id: ID of the maturity question to delete

        Returns:
            bool: True if deletion was successful
        """
        stmt = select(MaturityQuestion).where(
            MaturityQuestion.maturity_question_id == maturity_question_id)
        result = await self.session.execute(stmt)
        maturity_question = result.scalar_one_or_none()

        if not maturity_question:
            return False

        await self.session.delete(maturity_question)
        await self.session.commit()
        return True

    async def get(self, command: GetMaturityQuestion) -> Optional[MaturityQuestionResponse]:
        """Get a maturity question by ID or filters.

        Args:
            command: GetMaturityQuestion command

        Returns:
            Optional[MaturityQuestionResponse]: Maturity question data if found, None otherwise
        """
        stmt = select(MaturityQuestion)
        conditions = []

        if command.maturity_question_id:
            conditions.append(
                MaturityQuestion.maturity_question_id == command.maturity_question_id)
        if command.category:
            conditions.append(MaturityQuestion.category == command.category)
        if command.question_type:
            conditions.append(
                MaturityQuestion.question_type == command.question_type)
        if command.axis_id:
            conditions.append(MaturityQuestion.axis_id == command.axis_id)
        if command.industry_id:
            conditions.append(MaturityQuestion.industry_id == command.industry_id)

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self.session.execute(stmt)
        maturity_question = result.scalar_one_or_none()

        if not maturity_question:
            return None

        return MaturityQuestionResponse(
            maturity_question_id=maturity_question.maturity_question_id,
            question_text=maturity_question.question_text,
            question_type=maturity_question.question_type,
            question_order=maturity_question.question_order,
            category=maturity_question.category,
            axis_id=maturity_question.axis_id,
            industry_id=maturity_question.industry_id
        )

    async def list_all(
        self,
        category: Optional[str] = None,
        question_type: Optional[str] = None,
        axis_id: Optional[int] = None,
        industry_id: Optional[int] = None
    ) -> List[MaturityQuestionResponse]:
        """List all maturity questions, optionally filtered.

        Args:
            category: Optional category filter
            question_type: Optional question type filter
            axis_id: Optional axis ID filter

        Returns:
            List[MaturityQuestionResponse]: List of maturity questions
        """
        stmt = select(MaturityQuestion)

        if category:
            stmt = stmt.where(MaturityQuestion.category == category)
        if question_type:
            stmt = stmt.where(MaturityQuestion.question_type == question_type)
        if axis_id:
            stmt = stmt.where(MaturityQuestion.axis_id == axis_id)
        if industry_id:
            stmt = stmt.where(MaturityQuestion.industry_id == industry_id)

        result = await self.session.execute(stmt)
        maturity_questions = result.scalars().all()

        return [
            MaturityQuestionResponse(
                maturity_question_id=q.maturity_question_id,
                question_text=q.question_text,
                question_type=q.question_type,
                question_order=q.question_order,
                category=q.category,
                axis_id=q.axis_id,
                industry_id=q.industry_id
            )
            for q in maturity_questions
        ]

    async def get_questions_with_response(
        self,
        category: Optional[str] = None,
        question_type: Optional[str] = None,
        axis_id: Optional[int] = None,
        industry_id: Optional[int] = None,
        maturity_question_id: Optional[int] = None,
    ) -> List[Question]:
        """
        Get questions with options derived from existing agent responses.
        
        Returns:
            List[Question]: List of questions with their unique response options
        """
        where_clauses = []
        params = {}
        
        if category:
            where_clauses.append("mq.category = :category")
            params['category'] = category
        if question_type:
            where_clauses.append("mq.question_type = :question_type")
            params['question_type'] = question_type
        if axis_id:
            where_clauses.append("mq.axis_id = :axis_id")
            params['axis_id'] = axis_id
        if industry_id:
            where_clauses.append("mq.industry_id = :industry_id")
            params['industry_id'] = industry_id
        if maturity_question_id:
            where_clauses.append("mq.maturity_question_id = :maturity_question_id")
            params['maturity_question_id'] = maturity_question_id
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        schema = DatabaseSettings().local_settings.DB_SCHEMA
        query = text(f"""
            SELECT 
                mq.maturity_question_id AS id,
                mq.question_text,
                json_agg(json_build_object(
                    'id', mar.maturity_agent_response_id,
                    'text', mar.response_text,
                    'score', 0 
                )) options
            FROM {schema}.maturity_questions mq 
            JOIN {schema}.maturity_agent_responses mar ON mq.maturity_question_id = mar.maturity_question_id
            LEFT JOIN {schema}.industries i ON mq.industry_id = i.industry_id
            LEFT JOIN {schema}.ambitus a ON a.ambitus_id = mq.ambitus_id
            {where_clause}
            GROUP BY mq.maturity_question_id, mq.question_text, mq.ambitus_id, mq.question_order
            ORDER BY mq.ambitus_id, mq.question_order
        """)
        
        result = await self.session.execute(query, params)
        return [

            # Create Question object
            Question(
                id=doc.id,
                text=doc.question_text,
                options=[
                    QuestionOption(
                        id=int(line.get('id')), 
                        text=line.get('text'),
                        score=0
                    )
                    for line in doc.options
                ],
                category=None,
                subset=None
            )
            for doc in result.all()
        ]
        
