from sqlalchemy import Column, Integer, ForeignKey, Boolean
from dal.database import Base


class UserList(Base):
    __tablename__ = "user_lists"
    
    user_list_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer,ForeignKey("users.user_id"))
    shop_list_id = Column(Integer,ForeignKey("shop_lists.shop_list_id"))
    is_adm = Column(Boolean, default=False)
    is_nutritionist = Column(Boolean, default=False)
