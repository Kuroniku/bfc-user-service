import datetime

from sqlalchemy import Integer, Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped


class BaseModel(DeclarativeBase):
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)


class TimestampedModelMixin(object):
    created_at: Mapped[datetime.datetime] = Column(
        DateTime,
        default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = Column(
        DateTime,
        default=func.now()
    )
