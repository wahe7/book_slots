from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.router import router
from src.db.database import SessionLocal, engine
from src.db import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router with prefix
app.include_router(router, prefix="/api")

# You can now remove route logic from here and keep everything modular inside `src/routes/` and `src/services/`
