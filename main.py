from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String, Integer

app = FastAPI()

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# A SQLAlchemny ORM Character
class DBCharacter(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    allegiance = Column(String, nullable=True)
    lightSaber = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# A Pydantic Character
class Character(BaseModel):
    id: int
    name: Optional[str] = None
    allegiance: Optional[str] = None
    lightSaber: Optional[str] = None

    class Config:
        orm_mode = True

# Methods for interacting with the database
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

# Routes for interacting with the API
@app.post('/api/characters/', response_model=Character)
def create_characters_view(character: Character, db: Session = Depends(get_db)):
    db_character = create_character(db, character)
    return db_character

@app.get('/api/characters', response_model=List[Character])
def get_characters_view(db: Session = Depends(get_db)):
    return get_characters(db)

@app.get('/api/characters/{character_id}')
def get_characters_view(character_id: int, db: Session = Depends(get_db)):
    return get_character(db, character_id)

@app.get('/api/')
async def root():
    return {'message': 'Hello World!'}