from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.movies import router as movie_router

app = FastAPI(
    title="MovieHub API",
    description="High-end Movie Aggregator API",
    version="1.0.0"
)

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(movie_router)

@app.get("/")
async def root():
    return {"message": "Welcome to MovieHub API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
