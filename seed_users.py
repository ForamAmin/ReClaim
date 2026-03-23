from backend.database import SessionLocal
from backend.models import User

db = SessionLocal()

users = [
    User(email="admin@uni.edu", password="adminpass", role="admin"),
    User(email="Shelja@uni.edu", password="sheljapass", role="student"),
    User(email="Foram@uni.edu", password="forampass", role="student"),
    User(email="Janaki@uni.edu", password="janakipass", role="student"),
    User(email="Jaini@uni.edu", password="jainipass", role="student"),
    User(email="Tara@uni.edu", password="tarapass", role="student"),
]

db.add_all(users)
db.commit()
db.close()
print("Users seeded!")
