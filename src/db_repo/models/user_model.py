import datetime

from sqlalchemy import Column, DateTime, Text, String, Date
from sqlalchemy.orm import Mapped

from .base import BaseModel, TimestampedModelMixin


class UserModel(BaseModel, TimestampedModelMixin):
    __tablename__ = 'user'

    firstname: Mapped[str] = Column(
        String(100),
    )
    lastname: Mapped[str] = Column(
        String(100),
    )
    description: Mapped[str | None] = Column(
        Text,
        nullable=True,
        default=None
    )
    birthday: Mapped[datetime.date] = Column(
        Date,
        nullable=True,
    )

    profile_link: Mapped[str] = Column(
        String(42),
        nullable=True,
        default=None
    )
    phone: Mapped[str] = Column(
        String(11),
        nullable=True,
        default=None
    )

    deleted_at: Mapped[datetime.datetime | None] = Column(
        DateTime,
        nullable=True,
        default=None
    )
