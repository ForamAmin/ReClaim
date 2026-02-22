from sqlalchemy.orm import Session
from backend import models
from datetime import datetime

def get_all_items(db: Session, exclude_finder_id: int | None = None):
    """Fetches all items that are OPEN (Active found items)."""
    query = db.query(models.Item).filter(models.Item.status == "OPEN")
    if exclude_finder_id is not None:
        query = query.filter(models.Item.finder_id != exclude_finder_id)
    return query.all()

def get_items_by_finder(db: Session, user_id: int):
    """Fetches items reported by a specific user."""
    return db.query(models.Item).filter(models.Item.finder_id == user_id).all()

def get_claims_by_user(db: Session, user_id: int):
    """Fetches claims made by a specific user."""
    return db.query(models.Claim).join(models.Item).filter(models.Claim.user_id == user_id).all()

def create_test_item(db: Session, user_id: int):
    """Helper to create a dummy item if DB is empty."""
    test_item = models.Item(
        title="Blue Dell Laptop",
        description="Found in Library. Has a sticker.",
        category="Electronics",
        location_found="Library",
        image_url="/static/uploads/laptop.jpg",
        finder_id=user_id,
        ai_tags="laptop, dell"
    )
    db.add(test_item)
    db.commit()
    db.refresh(test_item)
    return test_item


def create_reported_item(
    db: Session,
    finder_id: int,
    title: str,
    description: str,
    category: str,
    location_found: str,
    image_url: str,
    date_found: datetime | None = None,
):
    item = models.Item(
        title=title,
        description=description,
        category=category,
        location_found=location_found,
        image_url=image_url,
        finder_id=finder_id,
        date_found=date_found,
        status="OPEN",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_open_item_by_id(db: Session, item_id: int):
    return (
        db.query(models.Item)
        .filter(models.Item.id == item_id, models.Item.status == "OPEN")
        .first()
    )


def has_user_claimed_item(db: Session, user_id: int, item_id: int) -> bool:
    return (
        db.query(models.Claim)
        .filter(models.Claim.user_id == user_id, models.Claim.item_id == item_id)
        .first()
        is not None
    )


def create_claim(db: Session, user_id: int, item_id: int, description_by_claimer: str):
    claim = models.Claim(
        user_id=user_id,
        item_id=item_id,
        description_by_claimer=description_by_claimer,
        status="PENDING",
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim

