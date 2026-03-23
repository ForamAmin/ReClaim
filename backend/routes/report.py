from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from backend.database import get_db
from backend.services import auth_service, item_service

#For Image blur 
from PIL import Image, ImageFilter
import io

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))
UPLOADS_DIR = FRONTEND_DIR / "static" / "uploads"

@router.get("/items/report", response_class=HTMLResponse)
def report_item_page(request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")

    if not user_email:
        return RedirectResponse(url="/login", status_code=303)

    user = auth_service.get_user_by_email(db, user_email)
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "report_item.html",
        {"request": request, "user": user, "user_email": user.email},
    )


@router.post("/items/report")
async def submit_report_item(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    location_found: str = Form(...),
    date_found: str | None = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=303)

    user = auth_service.get_user_by_email(db, user_email)
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    (UPLOADS_DIR / "originals").mkdir(parents=True, exist_ok=True)
    (UPLOADS_DIR / "blurs").mkdir(parents=True, exist_ok=True)
    
    file_bytes = await image.read()

    # Save original
    original_name = f"{uuid4().hex}-original.jpg"
    original_path = UPLOADS_DIR / "originals" / original_name
    with open(original_path, "wb") as f:
        f.write(file_bytes)

    # Save blurred version
    blurred_name = f"{uuid4().hex}-blurred.jpg"
    blurred_path = UPLOADS_DIR / "blurs" / blurred_name
    img = Image.open(io.BytesIO(file_bytes))
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=10))
    blurred_img.save(blurred_path)

    parsed_date = None
    if date_found:
        parsed_date = datetime.strptime(date_found, "%Y-%m-%d")

    item_service.create_reported_item(
        db=db,
        finder_id=user.id,
        title=title.strip(),
        description=description.strip(),
        category=category.strip(),
        location_found=location_found.strip(),
        image_url=f"/static/uploads/blurs/{blurred_name}",
        original_image_url=f"/static/uploads/originals/{original_name}",
        date_found=parsed_date,
    )

    request.session["message"] = "Report submitted successfully."
    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/items/{item_id}", response_class=HTMLResponse)
def item_detail_for_claim(item_id: int, request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=303)

    user = auth_service.get_user_by_email(db, user_email)
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    item = item_service.get_open_item_by_id(db, item_id)
    if not item:
        request.session["message"] = "Item not found or no longer open for claims."
        return RedirectResponse(url="/dashboard", status_code=303)

    return templates.TemplateResponse(
        "claim_item.html",
        {
            "request": request,
            "user_email": user.email,
            "item": item,
            "can_claim": item.finder_id != user.id,
        },
    )


@router.post("/items/{item_id}/claim")
def claim_item(
    item_id: int,
    request: Request,
    description_by_claimer: str = Form(...),
    db: Session = Depends(get_db),
):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=303)

    user = auth_service.get_user_by_email(db, user_email)
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    item = item_service.get_open_item_by_id(db, item_id)
    if not item:
        request.session["message"] = "Item not found or no longer open for claims."
        return RedirectResponse(url="/dashboard", status_code=303)

    if item.finder_id == user.id:
        request.session["message"] = "You cannot claim an item you reported."
        return RedirectResponse(url="/dashboard", status_code=303)

    if item_service.has_user_claimed_item(db, user.id, item.id):
        request.session["message"] = "You already submitted a claim for this item."
        return RedirectResponse(url="/dashboard", status_code=303)

    item_service.create_claim(
        db=db,
        user_id=user.id,
        item_id=item.id,
        description_by_claimer=description_by_claimer.strip(),
    )

    request.session["message"] = "Claim submitted successfully."
    return RedirectResponse(url="/dashboard", status_code=303)
