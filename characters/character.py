from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Integer

from db import Base

# A Pydantic Character
class Character(BaseModel):
    id: int
    name: Optional[str] = None
    allegiance: Optional[str] = None
    lightSaber: Optional[str] = None

    class Config:
        orm_mode = True

# A SQLAlchemny ORM Character
class DBCharacter(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    allegiance = Column(String, nullable=True)
    lightSaber = Column(String, nullable=True)

def get_character(db: Session, character_id: int):
    return db.query(DBCharacter).where(DBCharacter.id == character_id).first()

def get_characters(db: Session):
    return db.query(DBCharacter).all()

def create_character(db: Session, character: Character):
    db_character = DBCharacter(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)

    return db_character