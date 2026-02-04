from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend import database
from backend import models
from backend.routes import auth, dashboard # <--- Import the router
    
# 1. Setup DB
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ReClaim: UniConnect")

# 2. Setup Static Files
BASE_DIR = Path(__file__).resolve().parent 
FRONTEND_DIR = BASE_DIR.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

# 3. INCLUDE ROUTERS (The Clean Magic)
app.include_router(auth.router)
app.include_router(dashboard.router) 
# 4. Root Route (Optional redirect)
@app.get("/")
def home(request: Request):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/login")
