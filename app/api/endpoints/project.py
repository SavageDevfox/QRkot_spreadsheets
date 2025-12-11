from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_before_delete, check_project_before_edit, check_project_name)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.donation import donation_crud
from app.schemas.project import CreateProject, ProjectDB, UpdateProject
from app.crud.project import project_crud
from app.services.investment import make_investment

router = APIRouter()


@router.post(
    '/',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        project: CreateProject,
        session: AsyncSession = Depends(get_async_session)
):
    await check_project_name(session, project.name)
    new_project = await project_crud.create(session, project)

    sources = make_investment(
        new_project,
        await donation_crud.get_not_fully_invested(session))
    session.add_all(sources)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[ProjectDB]
)
async def get_projects(
        session: AsyncSession = Depends(get_async_session)
):
    projects = await project_crud.get_multi(session)
    return projects


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_before_delete(session, project_id)
    await project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        obj_in: UpdateProject,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_before_edit(
        session,
        project_id,
        obj_in.dict(exclude_unset=True)
    )
    if project_name := obj_in.dict().get('name'):
        await check_project_name(session, project_name)
    project = await project_crud.update(session, project, obj_in)
    session.add_all(make_investment(
        project, await donation_crud.get_not_fully_invested(session)))
    await session.commit()
    await session.refresh(project)
    return project
