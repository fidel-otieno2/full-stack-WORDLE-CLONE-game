import json
import os
from sqlalchemy.orm import Session
from ..models.word import Word
from ..config.settings import SessionLocal

def seed_words():
    """Seed the database with words from words.json"""
    db = SessionLocal()
    
    try:
        # Check if words already exist
        existing_words = db.query(Word).count()
        if existing_words > 0:
            print("Words already seeded. Skipping...")
            return
        
        # Load words from JSON file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        words_file = os.path.join(current_dir, 'words.json')
        
        with open(words_file, 'r') as f:
            words = json.load(f)
        
        # Add words to database
        for word in words:
            new_word = Word(word=word)
            db.add(new_word)
        
        db.commit()
        print(f"Successfully seeded {len(words)} words to the database.")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding words: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_words()
