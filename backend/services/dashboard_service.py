from sqlalchemy.orm import Session
from backend import models
from backend.services import item_service, admin_service

def build_dashboard_context(db: Session, user: models.User, request_obj):
    """
    Aggregates all data required for the dashboard.
    Returns a dictionary ready to be passed to the template.
    """
    
    # 1. Gather Data (Delegating to other services)
    public_items = item_service.get_all_items(db, exclude_finder_id=user.id)
    my_found = item_service.get_items_by_finder(db, user.id)
    my_claims = item_service.get_claims_by_user(db, user.id)

    # 2. Check Admin Status
    is_admin_user = (user.role == "admin")
    admin_data = None
    
    if is_admin_user:
        admin_data = admin_service.get_dashboard_stats(db)

    # 3. Package the "Contract"
    return {
        "request": request_obj, # Template needs request context
        "user_email": user.email,
        "is_admin": is_admin_user,
        "public_feed": public_items,
        "my_found_items": my_found,
        "my_claims": my_claims,
        "admin_stats": admin_data
    }