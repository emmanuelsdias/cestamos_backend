from typing import List, Union
from pydantic import BaseModel
from app.dto.output_dto import OutputBaseModel


class UserListCreate(BaseModel):
    user_id: int
    is_nutritionist: bool


class UserListStatus(BaseModel):
    is_nutritionist: Union[bool, None]
    is_adm: Union[bool, None]


class UserList(OutputBaseModel):
    user_id: int
    username: str
    is_adm: bool
    is_nutritionist: bool


class ItemCreate(BaseModel):
    name: str
    quantity: str


class ItemEdit(BaseModel):
    name: str
    quantity: str
    was_bought: bool


class Item(OutputBaseModel):
    item_id: int
    name: str
    quantity: str
    was_bought: bool


class ShopListCreate(BaseModel):
    name: str
    user_ids: List[int]

    is_template: bool


class ShopListEdit(BaseModel):
    name: str


class ShopListSummary(OutputBaseModel):
    shop_list_id: int
    name: str
    user_lists: List[UserList]


class ShopList(ShopListSummary):
    items: List[Item]
