from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path

# IMPORTS
from backend import database, models
from backend.routes import auth, dashboard, report
from backend.config import SECRET_KEY  # <--- NEW CLEAN IMPORT

# Setup DB
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ReClaim: UniConnect")

# 1. USE THE KEY FROM CONFIG
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Setup Static
BASE_DIR = Path(__file__).resolve().parent 
FRONTEND_DIR = BASE_DIR.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

# Include Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(report.router)

@app.get("/")
def home():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/login")