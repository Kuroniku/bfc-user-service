import datetime
import typing
from typing import Any

import pydantic
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.db_repo import UserModel


class UserData(pydantic.BaseModel):
    id: int | None = Field(default=None)

    firstname: str
    lastname: str
    description: str | None = Field(default=None)
    birthday: datetime.date

    profile_link: str
    phone: str

    @classmethod
    def _check_is_alpha(cls, v: str, info: ValidationInfo):
        if not v.isalpha():
            raise ValueError(f'{info.field_name} must not contain numbers')

    @classmethod
    def _check_is_alphanumeric(cls, v: str, info: ValidationInfo):
        if not v.isalnum():
            raise ValueError(f'{info.field_name} must not contain numbers')

    @classmethod
    def _check_no_longer(cls, length: int, v: str, info: ValidationInfo):
        if len(v) > length:
            raise ValueError(f'{info.field_name} is too long '
                             f'(max {length} symbols)')

    @field_validator('firstname')
    def _check_firstname(cls, v: str, info: ValidationInfo) -> str:
        cls._check_is_alpha(v, info)
        cls._check_no_longer(
            length=UserModel.firstname.property.columns[0].type.length,
            v=v,
            info=info
        )

        return v

    @field_validator('lastname')
    def _check_lastname(cls, v: str, info: ValidationInfo) -> str:
        cls._check_is_alpha(v, info)
        cls._check_no_longer(
            length=UserModel.lastname.property.columns[0].type.length,
            v=v,
            info=info
        )

        return v

    @field_validator("birthday")
    def _check_birthday(cls, v: datetime.date) -> datetime.date:
        if v > datetime.date.today():
            raise ValueError('Birthday cannot be in the future')
        return v

    @field_validator('profile_link')
    def _check_profile_link(cls, v: str, info: ValidationInfo) -> str:
        cls._check_is_alphanumeric(v, info)
        cls._check_no_longer(
            length=UserModel.profile_link.property.columns[0].type.length,
            v=v,
            info=info
        )

        return v

    @staticmethod
    def _cleanup_phone_number(v: str):
        allowed_symbols = "+-() "
        return "".join(
            filter(
                lambda x: x not in allowed_symbols,
                v
            )
        )

    @field_validator('phone')
    def _check_phone(cls, v: str, info: ValidationInfo) -> str:
        if len(v) > 100:
            raise ValueError(f'{info.field_name} is too long!')

        cls._check_is_alphanumeric(v, info)
        cls._check_no_longer(
            length=UserModel.phone.property.columns[0].type.length,
            v=v,
            info=info
        )

        return v

    def dict(self, *args, **kwargs) -> typing.Dict[str, Any]:
        dict_ = super().dict(*args, **kwargs)
        if self.id is None:
            dict_.pop("id")
        if self.description is None:
            dict_.pop("description")

        return dict_
