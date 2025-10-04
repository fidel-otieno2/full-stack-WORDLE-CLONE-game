import re
from typing import Optional

def validate_username(username: str) -> Optional[str]:
    """Validate username format"""
    if not username:
        return "Username cannot be empty"
    if len(username) < 3:
        return "Username must be at least 3 characters long"
    if len(username) > 20:
        return "Username must be at most 20 characters long"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return "Username can only contain letters, numbers, and underscores"
    return None

def validate_password(password: str) -> Optional[str]:
    """Validate password format"""
    if not password:
        return "Password cannot be empty"
    if len(password) < 6:
        return "Password must be at least 6 characters long"
    if len(password) > 50:
        return "Password must be at most 50 characters long"
    return None

# def validate_email(email: str) -> Optional[str]:
#     """Validate email format"""
#     if not email:
#         return "Email cannot be empty"
#     email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     if not re.match(email_pattern, email):
#         return "Please enter a valid email address"
#     return None
