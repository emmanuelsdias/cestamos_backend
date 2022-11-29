from fastapi import Depends
from sqlalchemy.orm import Session

from app.dal.item import ItemDal, ABCItemDal
from app.dal.user import UserDal, ABCUserDal
from app.dal.recipe import RecipeDal, ABCRecipeDal
from app.dal.shop_list import ShopListDal, ABCShopListDal
from app.dal.user_list import UserListDal, ABCUserListDal
from app.dal.invitation import InvitationDal, ABCInvitationDal
from app.dal.friendship import FriendshipDal, ABCFriendshipDal

from app.factories.db_session import get_db

def get_user_dal(
    db: Session = Depends(get_db)
) -> ABCUserDal:
    dal = UserDal(db)
    try:
        yield dal
    finally:
        pass


def get_recipe_dal(
    db: Session = Depends(get_db)
) -> ABCRecipeDal:
    dal = RecipeDal(db)
    try:
        yield dal
    finally:
        pass


def get_shop_list_dal(
    db: Session = Depends(get_db)
) -> ABCShopListDal:
    dal = ShopListDal(db)
    try:
        yield dal
    finally:
        pass


def get_invitation_dal(
    db: Session = Depends(get_db)
) -> ABCInvitationDal:
    dal = InvitationDal(db)
    try:
        yield dal
    finally:
        pass


def get_friendship_dal(
    db: Session = Depends(get_db)
) -> ABCFriendshipDal:
    dal = FriendshipDal(db)
    try:
        yield dal
    finally:
        pass


def get_item_dal(
    db: Session = Depends(get_db)
) -> ABCItemDal:
    dal = ItemDal(db)
    try:
        yield dal
    finally:
        pass


def get_user_list_dal(
    db: Session = Depends(get_db)
) -> ABCUserListDal:
    dal = UserListDal(db)
    try:
        yield dal
    finally:
        pass

