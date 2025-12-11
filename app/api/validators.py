from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import BAD_REQUEST_STATUS_CODE, NOT_FOUND_STATUS_CODE
from app.crud.project import project_crud


async def check_project_exists(
        session: AsyncSession,
        project_id: int
):
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=NOT_FOUND_STATUS_CODE, detail='Проект не найден')
    return project


async def check_project_name(
        session: AsyncSession,
        project_name: str
):
    project = await project_crud.get_project_by_name(session, project_name)
    if project is not None:
        raise HTTPException(
            BAD_REQUEST_STATUS_CODE,
            detail='Такое название проекта уже занято')


async def check_project_before_delete(
        session: AsyncSession,
        project_id: int
):
    project = await check_project_exists(session, project_id)
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=BAD_REQUEST_STATUS_CODE,
            detail=(
                'Нельзя удалять закрытый проект или проект, в который уже были'
                ' инвестированы средства.'
            )
        )
    return project


async def check_project_before_edit(
        session: AsyncSession,
        project_id: int,
        obj_in: dict
):
    project = await check_project_exists(session, project_id)
    new_full_amount = obj_in.get('full_amount', project.full_amount)
    if new_full_amount < project.invested_amount or project.fully_invested:
        raise HTTPException(BAD_REQUEST_STATUS_CODE)
    return project
