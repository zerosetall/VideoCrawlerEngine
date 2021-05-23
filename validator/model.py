

from pydantic import BaseModel, BaseConfig


class ValidateOnlyConfig(BaseConfig):
    orm_mode = True


class ValidatorModel(BaseModel):
    __config__ = ValidateOnlyConfig

