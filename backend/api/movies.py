from fastapi import APIRouter, HTTPException, BackgroundTasks, Request, Response
from fastapi.responses import StreamingResponse
import requests
from services.provider_engine import orchestrator
from services.tmdb_service import tmdb_service
from services.youtube_service import youtube_service
from core.database import SessionLocal
from models import models
from core.config import settings

router = APIRouter(prefix="/movies", tags=["Movies"])

def perform_sync():
    # This is now largely obsolete since we are focusing on YT,
    # but we keep it for database consistency.
    pass

@router.post("/sync")
async def trigger_sync(background_tasks: BackgroundTasks):
    background_tasks.add_task(perform_sync)
    return {"message": "Synchronization started in background"}

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
        return tmdb_service.get_movie_details(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}/recommendations")
async def get_recommendations(movie_id: int):
    try:
        return tmdb_service.get_recommendations(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}/sources")
async def get_movie_sources(movie_id: int, title: str):
    """
    SUPER-FAST AUTOMATED DISCOVERY:
    Focuses exclusively on YouTube for full movies.
    """
    try:
        sources = []
        
        # 1. Focus only on YouTube Discovery (Removed Thenkiri)
        yt_movies = youtube_service.search_full_movies(title)
        if yt_movies:
            best_yt = yt_movies[0]
            # Relative path for frontend to handle
            yt_download_path = f"/movies/youtube/download/{best_yt['id']}?title={title}"
            
            sources.append({
                "name": "YouTube HD", 
                "url": yt_download_path, 
                "type": "download",
                "is_youtube": True
            })
        
        return {"sources": sources}
    except Exception as e:
        print(f"Sources Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/youtube/download/{video_id}")
async def download_youtube_movie(video_id: str, title: str = "movie"):
    try:
        direct_url = youtube_service.get_direct_download_link(video_id)
        if not direct_url:
            raise HTTPException(status_code=404, detail="Could not extract direct video stream")

        response = requests.get(direct_url, stream=True)
        headers = {
            "Content-Disposition": f"attachment; filename={title.replace(' ', '_')}.mp4",
            "Content-Type": "video/mp4",
        }
        return StreamingResponse(
            response.iter_content(chunk_size=1024*1024),
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/youtube/search")
async def search_youtube_movies(title: str):
    try:
        movies = youtube_service.search_full_movies(title)
        return {"results": movies, "count": len(movies)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
