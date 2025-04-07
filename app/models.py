from sqlalchemy import Column, Integer, String
from database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=True, index=True)
    face_image_path = Column(String)