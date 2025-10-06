from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.settings import Base

class Game(Base):
    """Game model for storing each game session"""
    
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_word = Column(String(5), nullable=False)
    status = Column(String(20), default='in_progress')  # in_progress, won, lost
    attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships - use string references to avoid circular imports
    user = relationship("User", back_populates="games", foreign_keys=[user_id])
    guesses = relationship("Guess", back_populates="game")
    
    def __repr__(self):
        return f"<Game(id={self.id}, user_id={self.user_id}, status='{self.status}')>"