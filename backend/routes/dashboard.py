from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

# Imports
from backend.database import get_db # We can move the dependency to database.py to share it
from backend.services import auth_service, dashboard_service

router = APIRouter()

# Setup Templates (Shared logic)
BASE_DIR = Path(__file__).resolve().parent.parent 
FRONTEND_DIR = BASE_DIR.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    # 1. Identify User (The only logic the route keeps)
    # In a real app, we get ID from session/cookie here
    user_email = "student1@uni.edu" 
    user = auth_service.get_user_by_email(db, user_email)
    
    if not user:
        return RedirectResponse(url="/login")

    # 2. delegate EVERYTHING to the service
    context_data = dashboard_service.build_dashboard_context(db, user, request)

    # 3. Render
    return templates.TemplateResponse("dashboard.html", context_data)