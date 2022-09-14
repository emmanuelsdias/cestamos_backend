from typing import List
from pydantic import BaseModel
from app.dto.output_dto import OutputBaseModel


class UserListCreate(BaseModel):
    user_id: int
    is_nutritionist: bool


class UserList(OutputBaseModel):
    user_id: int
    username: str
    is_adm: bool
    is_nutritionist: bool


class ItemCreate(OutputBaseModel):
    name: str
    quantity: str


class Item(OutputBaseModel):
    item_id: int
    name: str
    quantity: str
    was_bought: bool


class ShopListCreate(BaseModel):
    name: str
    user_ids: List[int]

    is_template: bool


class ShopListSummary(OutputBaseModel):
    shop_list_id: int
    name: str
    user_lists: List[UserList]


class ShopList(ShopListSummary):
    items: List[Item]
