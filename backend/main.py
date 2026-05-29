from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.movies import router as movie_router
from api.favorites import router as favorites_router
from core.database import engine
from models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MovieHub API",
    description="High-end Movie Aggregator API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movie_router)
app.include_router(favorites_router)

@app.get("/")
async def root():
    return {"message": "Welcome to MovieHub API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
