from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.dal.database import Base

class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True, index=True)

    list_id = Column(Integer, ForeignKey("lists.list_id"))
    name = Column(String)
    quantity = Column(String)
    was_bought = Column(Boolean, default=False)