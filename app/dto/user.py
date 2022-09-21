from typing import List, Union
from pydantic import BaseModel
from app.dto.output_dto import OutputBaseModel

class UserCreate(BaseModel):
    username: Union[str, None]
    email: str
    password: str


class UserSummary(OutputBaseModel):
    user_id: int
    username: str


class User(UserSummary):
    email: str


class UserAuth(User):
    token: Union[str, None]

