from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.game import Game
from ..models.user import User

def get_user_stats(db: Session, user_id: int):
    """Get statistics for a specific user"""
    total_games = db.query(Game).filter(Game.user_id == user_id).count()
    games_won = db.query(Game).filter(Game.user_id == user_id, Game.status == 'won').count()
    games_lost = db.query(Game).filter(Game.user_id == user_id, Game.status == 'lost').count()
    
    win_percentage = (games_won / total_games * 100) if total_games > 0 else 0
    
    return {
        'total_games': total_games,
        'games_won': games_won,
        'games_lost': games_lost,
        'win_percentage': win_percentage
    }

def get_global_stats(db: Session):
    """Get global statistics"""
    total_users = db.query(User).count()
    total_games = db.query(Game).count()
    games_won = db.query(Game).filter(Game.status == 'won').count()
    
    return {
        'total_users': total_users,
        'total_games': total_games,
        'games_won': games_won,
    }