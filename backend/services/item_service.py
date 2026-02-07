from sqlalchemy.orm import Session
from backend import models

def get_all_items(db: Session):
    """Fetches all items that are OPEN (Active found items)."""
    return db.query(models.Item).filter(models.Item.status == "OPEN").all()

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

