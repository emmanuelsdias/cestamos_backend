from sqlalchemy import Column, Integer, String, ForeignKey
from dal.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String(50))
    ingredients = Column(String)
    instructions = Column(String)
