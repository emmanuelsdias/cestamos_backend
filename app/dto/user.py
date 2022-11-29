from typing import List, Union
from pydantic import BaseModel
from app.dto.output_dto import OutputBaseModel

class UserSummary(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(BaseModel):
    username: Union[str, None]
    email: str
    password: str

class User(OutputBaseModel):
    user_id: int
    username: str
    email: str

class UserAuth(OutputBaseModel):
    user_id: int
    username: str
    email: str
    token: Union[str, None]

class UserEdit(BaseModel):
    username: str
    old_password: str
    password: str

class UserPasswordCheck(BaseModel):
    password: str