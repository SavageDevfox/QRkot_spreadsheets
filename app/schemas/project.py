from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra

from datetime import datetime


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CreateProject(ProjectBase):
    pass


class UpdateProject(ProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)


class ProjectDB(ProjectBase):
    id: int
    fully_invested: bool
    create_date: datetime
    invested_amount: int
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
