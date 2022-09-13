from fastapi import APIRouter
from fastapi import Depends

from app.services.shop_list import ABCShopListService
from app.factories.shop_list import get_shop_list_service

from app.dto.shop_list import ShopList, ShopListCreate, ShopListSummary
from typing import List


router = APIRouter()

@router.get("/", response_model=List[ShopListSummary])
async def get_shop_lists(
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service)
):
    return shop_list_service.get_shop_lists(token)

@router.post("/", response_model=ShopListSummary)
async def create_shop_list(
    shop_list: ShopListCreate,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service)
):
    return shop_list_service.create_shop_list(shop_list, token)

@router.get("/{shop_list_id}", response_model=ShopList)
async def get_shop_list_by_id(
    shop_list_id: int,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service)
):
    return shop_list_service.get_shop_list_by_id(shop_list_id, token)
