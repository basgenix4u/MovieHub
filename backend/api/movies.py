from fastapi import APIRouter, HTTPException
from services.tmdb_service import tmdb_service

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/trending")
async def get_trending():
    try:
        return tmdb_service.get_trending_movies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_movies(query: str):
    try:
        return tmdb_service.search_movies(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}")
async def get_movie(movie_id: int):
    try:
        return tmdb_service.get_movie_details(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}/recommendations")
async def get_recommendations(movie_id: int):
    try:
        return tmdb_service.get_recommendations(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
