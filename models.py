from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    title = Column(String)
    cuisine = Column(String)
    difficulty = Column(String)

    ingredients = Column(JSON)
    instructions = Column(JSON)
    nutrition = Column(JSON)
    substitutions = Column(JSON)
    shopping_list = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
