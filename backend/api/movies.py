from fastapi import APIRouter, HTTPException, BackgroundTasks, Request, Response
from fastapi.responses import StreamingResponse
import requests
from services.provider_engine import orchestrator
from services.tmdb_service import tmdb_service
from services.scraper_service import scraper_service
from services.youtube_service import youtube_service
from core.database import SessionLocal
from models import models
from core.config import settings

router = APIRouter(prefix="/movies", tags=["Movies"])

def perform_sync():
    db = SessionLocal()
    try:
        scraped_movies = scraper_service.sync_latest_movies()
        for sm in scraped_movies:
            tmdb_res = tmdb_service.search_movies(sm['title'])
            if tmdb_res.get('results'):
                best_match = tmdb_res['results'][0]
                movie_id = best_match['id']
                movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
                if not movie:
                    movie = models.Movie(id=movie_id)
                    db.add(movie)
                movie.title = best_match['title']
                movie.overview = best_match.get('overview')
                movie.poster_path = best_match.get('poster_path')
                movie.backdrop_path = best_match.get('backdrop_path')
                movie.release_date = best_match.get('release_date')
                movie.vote_average = str(best_match.get('vote_average'))
                movie.source_url = sm['url']
                db.commit()
        return len(scraped_movies)
    except Exception as e:
        print(f"Sync Task Error: {e}")
        return 0
    finally:
        db.close()

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
    AUTOMATED DISCOVERY ENGINE:
    Finds streaming and download sources from multiple providers.
    """
    try:
        sources = []
        
        # 1. Get sources from existing providers
        results = await orchestrator.universal_search(title)
        for res in results:
            url = res.get('url')
            if url:
                direct_link = scraper_service.resolve_direct_download(url)
                if direct_link != url:
                    sources.append({"name": "Direct Download", "url": direct_link, "type": "download"})
                sources.append({"name": "Thenkiri", "url": url, "type": "stream"})
        
        # 2. AUTOMATIC YOUTUBE DISCOVERY
        yt_movies = youtube_service.search_full_movies(title)
        if yt_movies:
            best_yt = yt_movies[0]
            # We use a relative path for the download link so the frontend 
            # can prepend the correct base URL.
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
