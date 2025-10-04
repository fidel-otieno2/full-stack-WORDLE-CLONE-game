from sqlalchemy import Column, Integer, String
from ..config.settings import Base

class Word(Base):
    """Word model for storing valid 5-letter words"""
    
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(5), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Word(id={self.id}, word='{self.word}')>"