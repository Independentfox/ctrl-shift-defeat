import sys
from pathlib import Path

# Add backend dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from routes import session, stage, agent, download

app = FastAPI(title="CO-FOUNDER AI", version="1.0.0")

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router)
app.include_router(stage.router)
app.include_router(agent.router)
app.include_router(download.router)


@app.get("/")
async def root():
    return {"name": "CO-FOUNDER AI", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
