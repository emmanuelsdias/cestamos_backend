from fastapi import APIRouter
from fastapi import Depends

from app.services.item import ABCItemService
from app.factories.item import get_item_service

from app.dto.shop_list import Item, ItemEdit
from typing import List


router = APIRouter()

@router.put("/{item_id}", response_model=Item)
async def edit_item(
    item_data: ItemEdit,
    token: str = None,
    item_service: ABCItemService = Depends(get_item_service)
):
    return item_service.edit_item(token, item_data)
