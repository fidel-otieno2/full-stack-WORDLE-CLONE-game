from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.word import Word

def get_random_word(db: Session):
    """Retrieve a random word from the database."""
    return db.query(Word).order_by(func.random()).first()

def add_word(db: Session, word: str):
    """Add a new word to the database."""
    new_word = Word(word=word)
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word