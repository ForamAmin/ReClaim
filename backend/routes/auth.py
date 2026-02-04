from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from backend.database import SessionLocal
from backend.services import auth_service
router = APIRouter()

# Setup Templates again (Traffic cops need to know where HTML is)
BASE_DIR = Path(__file__).resolve().parent.parent 
FRONTEND_DIR = BASE_DIR.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# Dependency
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- ROUTES ---

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
    # USE THE NEW AUTH CHECK
    user = auth_service.authenticate_user(db, email, password)
    
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "message": "Invalid Email or Password." # Generic error is safer
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_email": user.email
    })