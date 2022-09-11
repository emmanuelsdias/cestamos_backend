from fastapi import Depends
from sqlalchemy.orm import Session

from app.dal.user import UserDal, ABCUserDal
from app.dal.recipe import RecipeDal, ABCRecipeDal
from app.dal.list import ListDal, ABCListDal

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

def get_list_dal(
    db: Session = Depends(get_db)
) -> ABCListDal:
    dal = ListDal(db)
    try:
        yield dal
    finally:
        pass