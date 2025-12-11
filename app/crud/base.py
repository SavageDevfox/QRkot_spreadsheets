from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def create(
            self,
            session: AsyncSession,
            obj_in,
            user=None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession
    ):
        return (
            await session.scalars(select(self.model))
        ).all()

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get(
            self,
            obj_id,
            session: AsyncSession
    ):
        db_obj = await session.get(self.model, obj_id)
        return db_obj

    async def update(
            self,
            session: AsyncSession,
            db_obj,
            obj_in
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def get_not_fully_invested(
            self,
            session: AsyncSession
    ):
        return (
            await session.scalars(
                select(self.model).
                where(self.model.fully_invested.is_(False))
                .order_by(self.model.create_date.asc())
            )
        ).all()
