from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse # <--- Vital import
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.database import get_db
from pathlib import Path

# Service Imports
from backend.services import auth_service

router = APIRouter()

# Setup Templates
BASE_DIR = Path(__file__).resolve().parent.parent 
FRONTEND_DIR = BASE_DIR.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# --- PUBLIC ROUTES ---

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def perform_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # 1. Check Credentials
    user = auth_service.authenticate_user(db, email, password)
    
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "message": "Invalid Email or Password."
        })

    # 2. LOGIN SUCCESS: Give them the Wristband (Cookie)
    request.session["user_email"] = user.email  # <--- SAVING TO COOKIE
    
    # 3. Redirect to Dashboard (Browser keeps the cookie)
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/logout")
def logout(request: Request):
    # Cut the wristband
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@router.get("/about")
def about_page(request: Request):
    # Check if they have a wristband, just to show their name in Navbar
    user_email = request.session.get("user_email") # Returns None if not logged in
    
    return templates.TemplateResponse("about.html", {
        "request": request,
        "user_email": user_email # Navbar uses this to decide what to show
    })