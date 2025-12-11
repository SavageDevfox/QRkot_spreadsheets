from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Integer, Boolean

from app.core.db import Base


class DistributionModel(Base):
    __abstract__ = True

    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0)
    full_amount = Column(Integer, nullable=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('full_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount')
    )

    def __repr__(self):
        return (
            f'{type(self)}\n'
            f'{self.invested_amount}/{self.full_amount}, '
            f'{self.create_date} - {self.close_date}'
        )
