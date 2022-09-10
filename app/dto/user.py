from typing import List, Union
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    user_id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    user_id: int
    username: str
    email: str
    token: Union[str, None]

    class Config:
        orm_mode = True