from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.dal.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    token = Column(String, unique=True, index=True)


