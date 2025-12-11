from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.crud.project import project_crud
from app.schemas.donation import (
    DonationDBPartial, DonationCreate, DonationDBFull)
from app.models import User
from app.services.investment import make_investment

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBPartial
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(session, donation, user)
    session.add_all(make_investment(
        new_donation,
        await project_crud.get_not_fully_invested(session))
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDBPartial]
)
async def get_donations_by_user(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_donations_by_user(session, user)
    return donations


@router.get(
    '/',
    response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations
