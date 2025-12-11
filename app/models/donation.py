from sqlalchemy import (
    Column, ForeignKey, Integer, String
)

from app.models.base import DistributionModel


class Donation(DistributionModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String, nullable=True)

    def __repr__(self):
        return f'{super().__repr__()}\n{self.user_id} - {self.comment}'
