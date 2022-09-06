from sqlalchemy import Column, Integer, String, Boolean
from app.dal.database import Base

class List(Base):
    __tablename__ = "lists"
    
    list_id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String)
    is_template = Column(Boolean, default=False)