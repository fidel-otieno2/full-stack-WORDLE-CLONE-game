from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from sqlalchemy.orm import Session
from ..services.game_service import get_game, make_guess, update_game_status, clear_user_current_game
from ..models.guess import Guess
from ..utils.helpers import get_word_feedback

console = Console()

def play_game(db: Session, game_id: int):
    """Main game loop - handles both new and resumed games"""
    # Get the game from database
    game = get_game(db, game_id)
    
    if not game:
        console.print("[red]Error: Game not found![/red]")
        return
    
    console.clear()
    
    if game.status == 'in_progress':
        console.print("[bold]🎮 Resuming your game...[/bold]")
        # Show previous guesses
        previous_guesses = db.query(Guess).filter(Guess.game_id == game_id).order_by(Guess.position).all()
        if previous_guesses:
            console.print("[bold]Your previous guesses:[/bold]")
            for guess in previous_guesses:
                display_feedback(guess.guess_word, guess.feedback)
    else:
        console.print("[bold]🎮 Starting a new game...[/bold]")
    
    attempts = game.attempts
    max_attempts = 6
    
    while attempts < max_attempts:
        guess = Prompt.ask(f"Attempt {attempts + 1}/{max_attempts}: Enter your guess")
        
        if len(guess) != 5:
            console.print("[red]Please enter a 5-letter word.[/red]")
            continue
        
        feedback = get_word_feedback(guess, game.target_word)
        display_feedback(guess, feedback)
        
        # Save the guess to the database
        make_guess(db, game.id, guess, attempts + 1)
        
        if feedback == ['correct'] * 5:
            console.print("[green]Congratulations! You've guessed the word![/green]")
            update_game_status(db, game.id, 'won')
            clear_user_current_game(db, game.user_id)  # Clear current game when finished
            break
        
        attempts += 1
    
    if attempts == max_attempts:
        console.print(f"[red]Game Over! The word was: {game.target_word}[/red]")
        update_game_status(db, game.id, 'lost')
        clear_user_current_game(db, game.user_id)  # Clear current game when finished

def display_feedback(guess: str, feedback: list):
    """Display feedback for the guess"""
    table = Table(title="Guess Feedback")
    table.add_column("Letter", style="cyan")
    table.add_column("Feedback", style="cyan")
    
    for letter, result in zip(guess, feedback):
        if result == 'correct':
            table.add_row(letter, "[green]correct[/green]")
        elif result == 'present':
            table.add_row(letter, "[yellow]present[/yellow]")
        else:
            table.add_row(letter, "[red]absent[/red]")
    
    console.print(table)