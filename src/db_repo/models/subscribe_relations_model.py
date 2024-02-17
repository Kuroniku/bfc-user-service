from sqlalchemy import Column, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel, TimestampedModelMixin
from .user_model import UserModel


class SubscribeRelationsModel(BaseModel, TimestampedModelMixin):
    __tablename__ = 'subscribe_relations'

    id: Mapped[int] = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = Column(
        Integer,
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
        ),
        nullable=False
    )
    user: Mapped["UserModel"] = relationship(UserModel)

    subscriber_id: Mapped[int] = Column(
        Integer,
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
        ),
        nullable=False
    )
    subscriber: Mapped["UserModel"] = relationship(UserModel)

    to_confirm: Mapped[bool]
