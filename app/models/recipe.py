from sqlalchemy import Column, Integer, String, ForeignKey
from app.dal.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, Primary_key = True, index = True)

    user_id = Column(Integer, ForeignKey("users.user_id"))
    ingredients = Column(String)
    instructions = Column(String)