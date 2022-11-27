from sqlalchemy import Column, Integer, String, Boolean
from app.dal.database import Base

class ShopList(Base):
    __tablename__ = "shop_lists"
    
    shop_list_id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String)
    is_template = Column(Boolean, default=False)