from sqlalchemy.orm import Session
from backend import models

def get_user_by_email(db: Session, email: str):
    """Worker function: Just finds the user."""
    return db.query(models.User).filter(models.User.email == email).first()

def check_user_exists(db: Session, email: str) -> bool:
    """Worker function: Returns True if user exists."""
    user = get_user_by_email(db, email)
    return user is not None

def authenticate_user(db: Session, email: str, password: str):
    """Worker: Checks if email exists AND password matches."""
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        return None  # User not found
    
    if user.password != password:
        return None  # Wrong password
        
    return user  # Success!