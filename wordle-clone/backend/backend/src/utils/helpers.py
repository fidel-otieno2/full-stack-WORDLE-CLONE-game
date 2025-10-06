import random
import string
from typing import List

def generate_random_string(length: int = 8) -> str:
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def validate_word(word: str, word_length: int = 5) -> bool:
    """Validate if a word meets the criteria"""
    if len(word) != word_length:
        return False
    if not word.isalpha():
        return False
    return True

def get_word_feedback(guess: str, target: str) -> List[str]:
    """
    Get feedback for a guess compared to target word
    Returns list of feedback codes: 'correct', 'present', 'absent'
    """
    feedback = ['absent'] * len(target)
    target_letters = list(target)
    guess_letters = list(guess)
    
    # First pass: mark correct letters
    for i in range(len(target)):
        if guess_letters[i] == target_letters[i]:
            feedback[i] = 'correct'
            target_letters[i] = None  # Mark as used
            guess_letters[i] = None   # Mark as used
    
    # Second pass: mark present letters
    for i in range(len(guess)):
        if guess_letters[i] is not None:
            if guess_letters[i] in target_letters:
                feedback[i] = 'present'
                # Remove the first occurrence from target
                target_letters[target_letters.index(guess_letters[i])] = None
    
    return feedback
