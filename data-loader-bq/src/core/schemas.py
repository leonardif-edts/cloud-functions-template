import json
from typing import List, Type, TypeVar, Union
from datetime import datetime

from pydantic import BaseModel, Base64Bytes, ValidationError

T = TypeVar("T", bound=BaseModel)


# Model
class UserCategory(BaseModel):
    name: str
    id: str

class User(BaseModel):
    id: int
    role_id: int
    principal_code: str
    category: List[UserCategory]
    created_date: datetime
    last_modified_date: datetime

class PrincipalTier(BaseModel):
    principal_code: str
    tier_master_id: int
    created_date: datetime
    last_modified_date: datetime


# Validator
class DataSchema(BaseModel):
    table: str
    data: Union[
        User,
        PrincipalTier
    ]


# Exception
class InvalidDataException(Exception):
    description: str = "Invalid Request"
    err_msg: str

    def __init__(self, val_err: str, *args, **kwargs):
        err_desc = json.loads(val_err)
        self.err_msg = {
            "input": err_desc[0]["input"],
            "errors": err_desc
        }

        super().__init__(val_err, *args, **kwargs)


# Helper
class PubSubMessage(BaseModel):
    data: Base64Bytes

    class Config:
        extra = "allow"

class PubSubData(BaseModel):
    message: PubSubMessage

    class Config:
        extra = "allow"


def parse_data(data: dict, Model: Type[T]) -> T:
    pb_data = PubSubData.model_validate(data)
    message_content = json.loads(pb_data.message.data.decode())
    try:
        m = Model.model_validate(message_content)
    except ValidationError as err:
        raise InvalidDataException(err.json(indent=2))
    return m