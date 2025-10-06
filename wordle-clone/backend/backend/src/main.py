import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rich.console import Console
from src.config.settings import Base, SQLALCHEMY_DATABASE_URL, SessionLocal
#importing functions that handle the UI in the terminal when the game is ongoing
from src.views.game_view import play_game
from src.views.login_view import login_user
from src.views.menu_view import show_main_menu, show_statistics, show_instructions
from src.services.game_service import start_new_game
from src.services.word_service import get_random_word
from src.services.stats_service import get_user_stats
from src.data.seed_data import seed_words

console = Console()

def main():
    # Set up the database
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    
    # Seed the database with words
    seed_words()
    
    # Start a new database session
    db = SessionLocal()
    
    # User login and this function only takes place when a user has unfinished game
    user_id, ongoing_game = login_user(db)
    
    # Show the main menu
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            # Start a new game
            console.print("[bold green]Starting a new Wordle Game...[/bold green]")
            target_word_obj = get_random_word(db)
            new_game = start_new_game(db, user_id, target_word_obj.word)
            play_game(db, new_game.id)
        elif choice == "2":
            # Show statistics
            stats = get_user_stats(db, user_id)
            show_statistics(stats)
        elif choice == "3":
            # Show instructions
            show_instructions()
        elif choice == "4":
            console.print("[bold red]Exiting the game...[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()
