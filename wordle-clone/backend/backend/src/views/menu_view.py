from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from ..utils.cli_styling import console, print_fancy_panel

def show_main_menu():
    """Display the main menu"""
    console.clear()
    print_fancy_panel(
        "[title]🎯 WORDLE CLI GAME[/title]",
        title="Main Menu",
        style="menu"
    )
    
    console.print("\n[menu]Main Menu:[/menu]")
    console.print("[menu]1. 🎮 Start New Game[/menu]")
    console.print("[menu]2. 📊 View Statistics[/menu]")
    console.print("[menu]3. ℹ️  Game Instructions[/menu]")
    console.print("[menu]4. 🚪 Exit[/menu]")
    
    choice = Prompt.ask(
        "\n[menu]Select an option (1-4)[/menu]",
        choices=["1", "2", "3", "4"],
        default="1"
    )
    
    return choice

def show_game_menu():
    """Display the in-game menu"""
    console.print("\n[menu]Game Menu:[/menu]")
    console.print("[menu]1. 🔄 Make a Guess[/menu]")
    console.print("[menu]2. 🏃‍♂️ Give Up[/menu]")
    console.print("[menu]3. ↩️  Return to Main Menu[/menu]")
    
    choice = Prompt.ask(
        "[menu]Select an option (1-3)[/menu]",
        choices=["1", "2", "3"],
        default="1"
    )
    
    return choice

def show_instructions():
    """Display game instructions"""
    console.clear()
    print_fancy_panel(
        "[info]📖 GAME INSTRUCTIONS[/info]",
        title="How to Play Wordle",
        style="info"
    )
    
    instructions = """
    🎯 Objective: Guess the 5-letter word in 6 attempts or less.
    
    🟩 Green: Letter is correct and in the right position.
    🟨 Yellow: Letter is in the word but in the wrong position.
    ⬜ Gray: Letter is not in the word.
    
    💡 Tips:
    - Start with common vowels and consonants
    - Use process of elimination
    - Pay attention to letter positions
    
    Press Enter to return to the main menu...
    """
    
    console.print(instructions)
    input()

def show_statistics(stats: dict):
    """Display user statistics"""
    console.clear()
    print_fancy_panel(
        "[info]📊 YOUR STATISTICS[/info]",
        title="Game Performance Overview",
        style="info"
    )
    
    if stats['total_games'] == 0:
        console.print("[info]No games played yet. Start playing to see your stats![/info]")
    else:
        console.print(f"[info]🎮 Total Games: {stats['total_games']}[/info]")
        console.print(f"[info]✅ Games Won: {stats['games_won']}[/info]")
        console.print(f"[info]❌ Games Lost: {stats['games_lost']}[/info]")
        console.print(f"[info]📈 Win Percentage: {stats['win_percentage']:.1f}%[/info]")
    
    console.print("\n[info]Press Enter to continue...[/info]")
    input()
