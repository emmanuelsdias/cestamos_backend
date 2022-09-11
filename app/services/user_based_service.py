from app.dal.user import ABCUserDal
from fastapi import HTTPException

class UserBasedService:
    def __init__(self, user_dal: ABCUserDal):
        self.user_dal = user_dal

    def check_user_validity(self, token: str):
        if token is None:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        user = self.user_dal.get_user_by_token(token)
        if user is None:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        return user