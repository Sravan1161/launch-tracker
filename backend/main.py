from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import projects

# Creates tables on startup if they don't exist yet.
# Fine for a small project like this — would use Alembic migrations at scale.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Launch Tracker API",
    description="Track a product's journey from idea to launch.",
    version="1.0.0",
)

# Allow the React dev server and deployed frontend to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://frontend-mu-roan-13.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(projects.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "launch-tracker-api"}
