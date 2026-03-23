from sqlalchemy.orm import Session
from backend import models
from sqlalchemy import func

def get_dashboard_stats(db: Session):
    """Calculates totals for the Admin Panel."""
    return {
        "total_users": db.query(models.User).count(),
        "total_items": db.query(models.Item).count()
    }

def get_all_items_with_details(db: Session):
    """Fetches ALL items (including resolved) with finder details."""
    return db.query(models.Item).all()

def get_all_claims_with_details(db: Session):
    """Fetches ALL claims with item and claimer details."""
    return db.query(models.Claim).all()

def get_items_with_conflict_count(db: Session):
    """Returns items grouped with their claim count to identify conflicts."""
    items = db.query(models.Item).all()
    items_data = []
    for item in items:
        claims = db.query(models.Claim).filter(models.Claim.item_id == item.id).all()
        items_data.append({
            "item": item,
            "claims": claims,
            "claim_count": len(claims),
            "has_conflict": len(claims) > 1,
            "pending_claims": [c for c in claims if c.status == "PENDING"]
        })
    return items_data

def approve_claim(db: Session, claim_id: int):
    """Approves a claim and marks item as RESOLVED."""
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if claim:
        claim.status = "APPROVED"
        claim.item.status = "RESOLVED"
        db.commit()
        db.refresh(claim)
    return claim

def reject_claim(db: Session, claim_id: int):
    """Rejects a claim."""
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if claim:
        claim.status = "REJECTED"
        db.commit()
        db.refresh(claim)
    return claim

def resolve_conflict(db: Session, approved_claim_id: int, item_id: int):
    """Resolves conflict by approving one claim and rejecting others for same item."""
    # Approve the chosen claim
    claim = db.query(models.Claim).filter(models.Claim.id == approved_claim_id).first()
    if claim:
        claim.status = "APPROVED"
        
        # Reject all other claims for this item
        other_claims = db.query(models.Claim).filter(
            models.Claim.item_id == item_id,
            models.Claim.id != approved_claim_id
        ).all()
        for other_claim in other_claims:
            other_claim.status = "REJECTED"
        
        # Mark item as resolved
        item = db.query(models.Item).filter(models.Item.id == item_id).first()
        if item:
            item.status = "RESOLVED"
        
        db.commit()
        db.refresh(claim)
    return claim