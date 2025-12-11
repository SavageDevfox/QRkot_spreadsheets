from sqlalchemy import (
    Column, String, Text
)

from app.models.base import DistributionModel


class CharityProject(DistributionModel):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'{super().__repr__()}\nНазвание проекта: {self.name}'
