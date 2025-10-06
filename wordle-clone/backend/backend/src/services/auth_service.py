from sqlalchemy.orm import Session
from src.models.user import User

def get_or_create_test_user(db: Session):
    """Get or create a test user for the game"""
    # Check if test user exists
    test_user = db.query(User).filter(User.username == "test_user").first()
    
    if test_user:
        return test_user
    
    # Create new test user if it doesn't exist
    test_user = User(username="test_user", password_hash="test_password")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    return test_user
