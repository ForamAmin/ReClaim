from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

# Imports
from backend.database import get_db
from backend.services import auth_service, admin_service

router = APIRouter()

# Setup Templates
BASE_DIR = Path(__file__).resolve().parent.parent 
FRONTEND_DIR = BASE_DIR.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

@router.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    """Admin dashboard showing all items and claims."""
    user_email = request.session.get("user_email")
    
    if not user_email:
        return RedirectResponse(url="/login")

    # Fetch Real User Object
    user = auth_service.get_user_by_email(db, user_email)
    
    # Safety check
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login")
    
    # Check if admin
    if user.role != "admin":
        return RedirectResponse(url="/dashboard")

    # Fetch all data
    items_with_conflicts = admin_service.get_items_with_conflict_count(db)
    stats = admin_service.get_dashboard_stats(db)

    context_data = {
        "request": request,
        "user_email": user.email,
        "user_role": user.role,
        "items_with_conflicts": items_with_conflicts,
        "stats": stats,
        "message": request.session.pop("message", None),
    }

    return templates.TemplateResponse("admin.html", context_data)


@router.post("/admin/claim/{claim_id}/approve")
def approve_claim_route(claim_id: int, request: Request, db: Session = Depends(get_db)):
    """Admin approves a claim."""
    user_email = request.session.get("user_email")
    
    if not user_email:
        return RedirectResponse(url="/login")

    user = auth_service.get_user_by_email(db, user_email)
    
    if not user or user.role != "admin":
        return RedirectResponse(url="/dashboard")

    admin_service.approve_claim(db, claim_id)
    request.session["message"] = "Claim approved successfully!"
    
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/admin/claim/{claim_id}/reject")
def reject_claim_route(claim_id: int, request: Request, db: Session = Depends(get_db)):
    """Admin rejects a claim."""
    user_email = request.session.get("user_email")
    
    if not user_email:
        return RedirectResponse(url="/login")

    user = auth_service.get_user_by_email(db, user_email)
    
    if not user or user.role != "admin":
        return RedirectResponse(url="/dashboard")

    admin_service.reject_claim(db, claim_id)
    request.session["message"] = "Claim rejected successfully!"
    
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/admin/conflict/resolve")
def resolve_conflict_route(
    request: Request,
    approved_claim_id: int = Form(...),
    item_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Admin resolves a conflict by choosing which claim to approve."""
    user_email = request.session.get("user_email")
    
    if not user_email:
        return RedirectResponse(url="/login")

    user = auth_service.get_user_by_email(db, user_email)
    
    if not user or user.role != "admin":
        return RedirectResponse(url="/dashboard")

    admin_service.resolve_conflict(db, approved_claim_id, item_id)
    request.session["message"] = "Conflict resolved! Item marked as returned."
    
    return RedirectResponse(url="/admin", status_code=303)
