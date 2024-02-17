import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped

from .base import BaseModel, TimestampedModelMixin


class UserModel(BaseModel, TimestampedModelMixin):
    __tablename__ = 'user'

    firstname: Mapped[str]
    lastname: Mapped[str]
    description: Mapped[str | None]
    birthday: Mapped[datetime.datetime]

    profile_link: Mapped[str]
    phone: Mapped[str]

    deleted_at: Mapped[datetime.datetime | None] = Column(
        DateTime,
        nullable=True
    )
