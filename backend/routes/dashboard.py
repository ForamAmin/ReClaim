from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

# Imports
from backend.database import get_db
from backend.services import auth_service, dashboard_service

router = APIRouter()

# Setup Templates
BASE_DIR = Path(__file__).resolve().parent.parent 
FRONTEND_DIR = BASE_DIR.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    # 1. READ COOKIE (The Wristband Check)
    user_email = request.session.get("user_email") 
    
    if not user_email:
        # No wristband? Kick them out.
        return RedirectResponse(url="/login")

    # 2. Fetch Real User Object using the email from cookie
    user = auth_service.get_user_by_email(db, user_email)
    
    # Safety check: If cookie exists but user was deleted from DB
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login")

    # 3. Delegate to Service
    context_data = dashboard_service.build_dashboard_context(db, user, request)

    # 4. Render
    return templates.TemplateResponse("dashboard.html", context_data)