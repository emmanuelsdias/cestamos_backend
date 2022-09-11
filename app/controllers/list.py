from fastapi import APIRouter
from fastapi import Depends

from app.services.list import ABCListService
from app.factories.list import get_list_service

from app.dto.list import List, ListCreate, ListSummary
from typing import List


router = APIRouter()

@router.get("/", response_model=List[ListSummary])
async def get_lists(
    token: str = None,
    list_service: ABCListService = Depends(get_list_service)
):
    return list_service.get_lists(token)

@router.post("/", response_model=List)
async def create_list(
    list: ListCreate,
    token: str = None,
    list_service: ABCListService = Depends(get_list_service)
):
    return list_service.create_list(list, token)

@router.get("/{list_id}", response_model=List)
async def get_list_by_id(
    list_id: int,
    token: str = None,
    list_service: ABCListService = Depends(get_list_service)
):
    return list_service.get_list_by_id(list_id, token)
