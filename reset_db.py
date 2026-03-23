from backend.database import Base, engine
from backend.models import User, Item, Claim  # Import models to register them with Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Done!")
