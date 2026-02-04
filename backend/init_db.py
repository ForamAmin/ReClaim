from backend.database import engine, SessionLocal, Base
from backend.models import User, Item, Claim # Import your tables
from sqlalchemy.orm import Session

# 1. Create the Tables (if they don't exist)
Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    
    # Check if users already exist to avoid duplicates
    if db.query(User).first():
        print("Database already initialized!")
        return

    # 2. Define the Dummy Data
    dummy_users = [
        User(email="admin@uni.edu", password="adminpass", role="admin"), # The 1 Admin
        User(email="Shelja@uni.edu", password="sheljapass", role="student"),
        User(email="Foram@uni.edu", password="forampass", role="student"),
        User(email="Janaki@uni.edu", password="janakipass", role="student"),
        User(email="Jaini@uni.edu", password="jainipass", role="student"),
        User(email="Tara@uni.edu", password="tarapass", role="student"),
    ]

    # 3. Add to Database
    db.add_all(dummy_users)
    db.commit()
    print("✅ Successfully added 1 Admin and 5 Students.")
    db.close()

if __name__ == "__main__":
    init_db()