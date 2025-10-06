from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.settings import Base

class Guess(Base):
    """Guess model for storing each guess made in a game"""
    
    __tablename__ = 'guesses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    guess_word = Column(String(5), nullable=False)
    position = Column(Integer, nullable=False)  # The attempt number (1-6)
    feedback = Column(String(20))  # Feedback for the guess (e.g., 'GGYYB')
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    game = relationship("Game", back_populates="guesses")
    
    def __repr__(self):
        return f"<Guess(id={self.id}, game_id={self.game_id}, word='{self.guess_word}', feedback='{self.feedback}')>"
