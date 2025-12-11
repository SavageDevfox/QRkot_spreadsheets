from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.charity_project import CharityProject


class ProjectCRUD(CRUDBase):

    @staticmethod
    async def get_project_by_name(
            session: AsyncSession,
            project_name: str,
    ):
        return (
            await session.scalars(
                select(CharityProject).
                where(CharityProject.name == project_name))
        ).first()

    @staticmethod
    async def get_projects_by_completion_rate(
        session: AsyncSession,
    ):
        return (await session.scalars(
            select(CharityProject).
            where(CharityProject.fully_invested.is_(True)).
            order_by(
                extract(
                    'epoch',
                    CharityProject.close_date - CharityProject.create_date
                )
            )
        )).all()


project_crud = ProjectCRUD(CharityProject)
