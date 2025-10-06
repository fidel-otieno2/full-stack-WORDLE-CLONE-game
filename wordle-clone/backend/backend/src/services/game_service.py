from sqlalchemy.orm import Session
from ..models.game import Game
from ..models.guess import Guess
from ..models.user import User

def start_new_game(db: Session, user_id: int, target_word: str):
    """Start a new game and save it to the database."""
    new_game = Game(user_id=user_id, target_word=target_word)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    
    # Set this as the user's current game
    set_user_current_game(db, user_id, new_game.id)
    
    return new_game

def get_game(db: Session, game_id: int):
    """Retrieve a game by its ID."""
    return db.query(Game).filter(Game.id == game_id).first()

def make_guess(db: Session, game_id: int, guess_word: str, position: int):
    """Make a guess in a game and save it to the database."""
    # First, update the game's attempts counter
    game = db.query(Game).filter(Game.id == game_id).first()
    if game:
        game.attempts += 1
        db.commit()
    
    # Calculate feedback for the guess
    feedback_list = check_guess(game.target_word, guess_word)
    
    # Convert feedback list to string format (G=correct, Y=present, B=absent)
    feedback_str = ''.join([
        'G' if status == 'correct' else 
        'Y' if status == 'present' else 
        'B' 
        for status in feedback_list
    ])
    
    # Then create the guess with feedback
    new_guess = Guess(game_id=game_id, guess_word=guess_word, position=position, feedback=feedback_str)
    db.add(new_guess)
    db.commit()
    db.refresh(new_guess)
    return new_guess

def check_guess(target_word: str, guess_word: str):
    """Check a guess against the target word and return feedback."""
    feedback = ['absent'] * len(target_word)
    target_chars = list(target_word.upper())
    guess_chars = list(guess_word.upper())
    
    # First pass: check for correct letters in correct positions
    for i in range(len(target_chars)):
        if guess_chars[i] == target_chars[i]:
            feedback[i] = 'correct'
            target_chars[i] = None  # Mark as used
            guess_chars[i] = None   # Mark as used
    
    # Second pass: check for correct letters in wrong positions
    for i in range(len(guess_chars)):
        if guess_chars[i] is not None and guess_chars[i] in target_chars:
            feedback[i] = 'present'
            # Remove the first occurrence from target
            target_chars[target_chars.index(guess_chars[i])] = None
    
    return feedback

def update_game_status(db: Session, game_id: int, status: str):
    """Update the status of a game."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if game:
        game.status = status
        db.commit()
        db.refresh(game)
    return game

def set_user_current_game(db: Session, user_id: int, game_id: int):
    """Set the current game for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.current_game_id = game_id
        db.commit()
        db.refresh(user)
    return user

def clear_user_current_game(db: Session, user_id: int):
    """Clear the current game for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.current_game_id = None
        db.commit()
        db.refresh(user)
    return user

def get_user_current_game(db: Session, user_id: int):
    """Get the current game for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.current_game_id:
        return db.query(Game).filter(Game.id == user.current_game_id).first()
    return None