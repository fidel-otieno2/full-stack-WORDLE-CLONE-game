from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from rich.style import Style

# Custom theme for the Wordle game with fancy styling
custom_theme = Theme({
    "success": "bold green on #1a1a2e",
    "error": "bold red on #1a1a2e",
    "warning": "bold yellow on #1a1a2e",
    "info": "bold cyan on #1a1a2e",
    "highlight": "bold magenta on #1a1a2e",
    "menu": "bold #ff6b6b on #1a1a2e",
    "correct": "bold white on #4ecdc4",
    "present": "bold white on #ffd93d",
    "absent": "bold white on #6c757d",
    "background": "on #1a1a2e",
    "title": "bold #ff6b6b on #1a1a2e",
    "subtitle": "italic #f8f9fa on #1a1a2e",
    "border": "#4ecdc4",
})

console = Console(theme=custom_theme)

def set_terminal_background():
    """Set a fancy background for the terminal"""
    console.print("\n" * 2)  # Add some space
    console.print("[background]                                                          [/background]")
    console.print("[background]                 WELCOME TO WORDLE CLI                    [/background]")
    console.print("[background]                                                          [/background]")
    console.print("\n" * 2)

def print_fancy_panel(content, title="", style="info"):
    """Print content in a fancy panel with custom styling"""
    console.print(
        Panel.fit(
            content,
            title=title,
            style=style,
            border_style="border",
            padding=(1, 2)
        )
    )

def print_welcome():
    """Print a welcome message with fancy styling"""
    set_terminal_background()
    console.print(
        Panel.fit(
            "[title]🎯 WELCOME TO WORDLE CLI GAME![/title]",
            subtitle="[subtitle]Guess the 5-letter word challenge[/subtitle]",
            style="background",
            border_style="border"
        )
    )

def print_game_status(status_message, style="info"):
    """Print game status messages with styling"""
    console.print(f"[{style}]{status_message}[/{style}]")

def print_guess_feedback(guess, feedback):
    """Print guess feedback with color coding"""
    colored_guess = Text()
    for i, letter in enumerate(guess.upper()):
        if feedback[i] == 'correct':
            colored_guess.append(letter, style="correct")
        elif feedback[i] == 'present':
            colored_guess.append(letter, style="present")
        else:
            colored_guess.append(letter, style="absent")
        colored_guess.append(" ")
    
    console.print(colored_guess)

def print_game_over(word, won=False):
    """Print game over message"""
    if won:
        message = f"🎉 Congratulations! You guessed the word: [highlight]{word}[/highlight]"
        style = "success"
    else:
        message = f"😢 Game Over! The word was: [highlight]{word}[/highlight]"
        style = "error"
    
    console.print(
        Panel.fit(
            message,
            style=style,
            border_style="border"
        )
    )
