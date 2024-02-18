import datetime
import typing
from typing import Any

import pydantic
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.models import UserModel


class UserPutDTO(pydantic.BaseModel):
    firstname: str
    lastname: str
    description: str | None = Field(default=None)
    birthday: datetime.date

    profile_link: str | None = Field(default=None)
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
    def _check_profile_link(cls, v: str | None, info: ValidationInfo) -> str | None:
        if v is None:
            return v
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
        return {
            field_name: dict_[field_name]
            for field_name in self.__fields_set__
            if dict_[field_name] is not None
        }


class UserPatchDTO(UserPutDTO):
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    description: str | None = Field(default=None)
    birthday: datetime.date | None = Field(default=None)

    profile_link: str | None = Field(default=None)
    phone: str | None = Field(default=None)

    @field_validator('firstname')
    def _check_firstname(cls, v: str, info: ValidationInfo) -> str | None:
        if v is None:
            return v
        return super()._check_firstname(v, info)

    @field_validator('lastname')
    def _check_lastname(cls, v: str, info: ValidationInfo) -> str | None:
        if v is None:
            return v
        return super()._check_lastname(v, info)

    @field_validator("birthday")
    def _check_birthday(cls, v: datetime.date) -> datetime.date | None:
        if v is None:
            return v
        return super()._check_birthday(v)

    @field_validator('profile_link')
    def _check_profile_link(cls, v: str, info: ValidationInfo) -> str | None:
        if v is None:
            return v
        return super()._check_profile_link(v, info)

    @field_validator('phone')
    def _check_phone(cls, v: str, info: ValidationInfo) -> str | None:
        if v is None:
            return v
        return super()._check_phone(v, info)


class UserFullDTO(UserPutDTO):
    id: int | None = Field(default=None)
