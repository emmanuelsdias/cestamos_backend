from fastapi import APIRouter
from fastapi import Depends

from services.item import ABCItemService
from factories.item import get_item_service

from dto.shop_list import Item, ItemEdit
from typing import List


router = APIRouter()


@router.put("/{item_id}", response_model=Item)
async def edit_item(
    item_id: int,
    item_data: ItemEdit,
    token: str = None,
    item_service: ABCItemService = Depends(get_item_service),
):
    return item_service.edit_item(token, item_data, item_id)


@router.delete("/{item_id}", response_model=Item)
async def delete_item(
    item_id: int,
    token: str = None,
    item_service: ABCItemService = Depends(get_item_service),
):
    return item_service.delete_item(token, item_id)
