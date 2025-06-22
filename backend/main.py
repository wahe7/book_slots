from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.router import router

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

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Render"}

# You can now remove route logic from here and keep everything modular inside `src/routes/` and `src/services/`
