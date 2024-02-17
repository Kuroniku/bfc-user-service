from sqlalchemy import Column, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel, TimestampedModelMixin
from .user_model import UserModel


class FriendsRelationsModel(BaseModel, TimestampedModelMixin):
    __tablename__ = 'friends_relations'

    id: Mapped[int] = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_1_id: Mapped[int] = Column(
        Integer,
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
        ),
        nullable=False
    )
    user_1: Mapped["UserModel"] = relationship(UserModel)

    user_2_id: Mapped[int] = Column(
        Integer,
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
        ),
        nullable=False
    )
    user_2: Mapped["UserModel"] = relationship(UserModel)
