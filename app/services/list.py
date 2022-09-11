import abc
from pydantic import parse_obj_as

from app.dal.list import ABCListDal
from app.dal.user import ABCUserDal

from app.dto.list import List, ListCreate, ListSummary

from app.models.list import List as ListModel
from app.models.user import User as UserModel

from app.services.user_based_service import UserBasedService


from typing import List

class ABCListService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def get_lists(self, token) -> List[ListSummary]:
        """ Returns lists from user """
    
    @abc.abstractmethod
    def get_list_by_id(self, list_id) -> List:
        """ Return the list with given id """

    @abc.abstractmethod
    def create_list(self, list: ListCreate, token: str) -> List:
        """ Create a list """



class ListService(ABCListService):

    def __init__(
        self,
        list_dal: ABCListDal,
        user_dal: ABCUserDal,
    ):
        super().__init__(user_dal)
        self.dal = list_dal


    def get_lists(self, token) -> List[ListSummary]:
        user = self.check_user_validity(token)
        lists = self.dal.get_lists_from_user(user.user_id)
        return parse_obj_as(List[ListSummary], lists)

    def get_list_by_id(self, list_id: int, token: str) -> List:
        user = self.check_user_validity(token)

        list = self.dal.get_list_by_id(list_id)
        if user.user_id != list.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        return parse_obj_as(List, self.dal.get_list_by_id(list_id))

    def create_list(self, list: ListCreate, token: str) -> List:
        user = self.check_user_validity(token)
        
        db_list = ListModel(
            user_id=user.user_id,
            name = list.name,
            ingredients=list.ingredients,
            instructions=list.instructions,
        )
        created_list = self.dal.create_list(list=db_list)
        return List.from_orm(created_list)
    
    def update_list(self, list_id: int, list: ListCreate, token: str) -> List:
        user = self.check_user_validity(token)
        current_list = self.dal.get_list_by_id(list_id)
        if current_list is None:
            raise HTTPException(
                status_code=400, detail="List doesn't exist"
            )
        if user.user_id != current_list.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        db_list = ListModel(
            list_id=list_id,
            name = list.name,
            ingredients=list.ingredients,
            instructions=list.instructions,
        )
        saved_list = self.dal.update_list(db_list)
        return List.from_orm(saved_list)

    def delete_list(self, list_id: int, token: str) -> List:
        user = self.check_user_validity(token)
        current_list = self.dal.get_list_by_id(list_id)
        if current_list is None:
            raise HTTPException(
                status_code=400, detail="List doesn't exist"
            )
        if user.user_id != current_list.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        deleted_list = self.dal.delete_list(list_id)
        return List.from_orm(deleted_list)