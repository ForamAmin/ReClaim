from sqlalchemy.orm import Session
from backend import models

def get_dashboard_stats(db: Session):
    """Calculates totals for the Admin Panel."""
    return {
        "total_users": db.query(models.User).count(),
        "total_items": db.query(models.Item).count()
    }