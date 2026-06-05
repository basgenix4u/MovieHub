from fastapi import APIRouter, HTTPException
from services.provider_engine import orchestrator
from services.tmdb_service import tmdb_service

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/universal-search")
async def universal_search(q: str):
    try:
        results = await orchestrator.universal_search(q)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending")
async def get_trending():
    return tmdb_service.get_trending_movies()

@router.get("/{movie_id}")
async def get_movie(movie_id: int):
    try:
        return tmdb_//service.get_movie_details(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
