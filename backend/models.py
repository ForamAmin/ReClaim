from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

# 1. Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # <--- NEW COLUMN
    role = Column(String, default="student")
    
    # Relationships stay the same...
    reported_items = relationship("Item", back_populates="finder")
    claims = relationship("Claim", back_populates="claimer")
    
# 2. Items Table (The "Truth")
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False) # Public description
    category = Column(String, nullable=False)    # e.g., Electronics, Clothing
    location_found = Column(String, nullable=False)
    date_found = Column(DateTime(timezone=True), server_default=func.now())
    
    image_url = Column(String, nullable=False)   # Path to /static/uploads/...
    original_image_url = Column(String, nullable=True)
    
    # 🔒 HIDDEN AI TAGS (The Magic)
    ai_tags = Column(String, nullable=True) 

    status = Column(String, default="OPEN") # OPEN, PENDING, RESOLVED
    
    finder_id = Column(Integer, ForeignKey("users.id"))
    finder = relationship("User", back_populates="reported_items")
    
    claims = relationship("Claim", back_populates="item")

# 3. Claims Table (The "Proof")
class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    
    # The user's proof text
    description_by_claimer = Column(String, nullable=False)
    
    # 🧠 System calculated score (0-100)
    match_score = Column(Float, default=0.0)
    
    status = Column(String, default="PENDING") # PENDING, APPROVED, REJECTED
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    claimer = relationship("User", back_populates="claims")
    
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="claims")