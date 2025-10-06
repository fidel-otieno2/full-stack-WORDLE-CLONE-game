
from rich.console import Console
from sqlalchemy.orm import Session
from src.services.auth_service import get_or_create_test_user
from src.services.game_service import get_user_current_game
from ..utils.cli_styling import console, set_terminal_background

def login_user(db: Session):
    """Handle user login and check for ongoing games"""
    set_terminal_background()
    console.print("[title]Welcome to the Wordle Game![/title]")
    
    username = console.input("[menu]Enter your username: [/menu]")
    password = console.input("[menu]Enter your password: [/menu]")
    
    # Here you would typically validate the username and password
    # For now, we will just create or get the test user
    user = get_or_create_test_user(db)
    
    console.print(f"[highlight]Logged in as: {user.username}[/highlight]")
    
    # Check if user has an ongoing game
    ongoing_game = get_user_current_game(db, user.id)
    
    return user.id, ongoing_game
