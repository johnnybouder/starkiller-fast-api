from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session
from main import app
from db import get_db
from characters.character import Character

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

from characters.character import *