from datetime import datetime

from app.models.base import DistributionModel


def make_investment(
        target: DistributionModel,
        sources: list[DistributionModel]
) -> list[DistributionModel]:
    edited_sources = []
    for source in sources:
        edited_sources.append(source)
        res = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += res
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        if target.fully_invested:
            break
    return edited_sources
