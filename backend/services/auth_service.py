from sqlalchemy.orm import Session
from backend import models
# services/auth_service.py
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

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

def get_current_user_from_session(request: Request):
    # Retrieve the session ID from cookies
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        # If no cookie, the user is 'delusional' about being logged in
        return None
    
    # Logic to look up session_id in SQLite would go here
    # For now, return a dummy user or the session_id
    return session_id