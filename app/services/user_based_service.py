from dal.user import ABCUserDal
from fastapi import HTTPException
from models.user import User
from typing import Optional


class UserBasedService:
    def __init__(self, user_dal: ABCUserDal):
        self.user_dal = user_dal

    def raise_access_denied_error(self):
        raise HTTPException(status_code=403, detail="Access Denied")

    def check_user_validity(self, token: str) -> Optional[User]:
        if token is None:
            self.raise_access_denied_error()
        user = self.user_dal.get_user_by_token(token)
        if user is None:
            self.raise_access_denied_error()
        return user
