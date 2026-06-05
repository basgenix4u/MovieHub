from fastapi import APIRouter, HTTPException, BackgroundTasks
from services.provider_engine import orchestrator
from services.tmdb_service import tmdb_service
from services.scraper_service import scraper_service
from core.database import SessionLocal
from models import models

router = APIRouter(prefix="/movies", tags=["Movies"])

def perform_sync():
    """
    Syncs latest movies from Thenkiri and updates database with TMDB metadata.
    """
    db = SessionLocal()
    try:
        scraped_movies = scraper_service.sync_latest_movies()
        for sm in scraped_movies:
            # Find movie on TMDB to get metadata and ID
            tmdb_res = tmdb_service.search_movies(sm['title'])
            if tmdb_res.get('results'):
                best_match = tmdb_res['results'][0]
                movie_id = best_match['id']
                
                # Upsert movie in DB
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
    """
    Triggers a background synchronization of movies.
    """
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
    """
    Fetches recommended movies based on the current movie ID.
    """
    try:
        return tmdb_service.get_recommendations(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}/sources")
async def get_movie_sources(movie_id: int, title: str):
    """
    Finds streaming and download sources for a specific movie by title.
    """
    try:
        # Search for the movie title across providers
        results = await orchestrator.universal_search(title)
        
        sources = []
        for res in results:
            url = res.get('url')
            if url:
                # Try to resolve a direct download link
                direct_link = scraper_service.resolve_direct_download(url)
                
                # If the link changed, we have a direct download
                if direct_link != url:
                    sources.append({"name": "Direct Download", "url": direct_link, "type": "download"})
                
                # Also add the source page as a streaming option
                sources.append({"name": "Thenkiri", "url": url, "type": "stream"})
        
        return {"sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
