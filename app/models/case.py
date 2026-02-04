from sqlalchemy import Column, Integer, String, Text
from app.models.db import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    department = Column(String)
    emotion = Column(String)
