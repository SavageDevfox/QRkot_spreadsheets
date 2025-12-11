from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase

from app.models import Donation, User
from app.schemas.donation import DonationDBPartial


class DonationCRUD(CRUDBase):

    @staticmethod
    async def get_donations_by_user(
        session: AsyncSession,
        user: User
    ) -> list[DonationDBPartial]:
        return (
            await session.scalars(
                select(Donation).
                where(Donation.user_id == user.id)
            )
        ).all()


donation_crud = DonationCRUD(Donation)
