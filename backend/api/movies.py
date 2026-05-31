from fastapi import APIRouter, HTTPException
from services.tmdb_service import tmdb_service
from services.scraper_service import scraper_service

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/trending")
async def get_trending():
    # Mix TMDB trending with Scraped latest movies for a "Live" feel
    tmdb_movies = tmdb_service.get_trending_movies().get('results', [])
    scraped_movies = scraper_service.fetch_thenkiri_latest()
    
    # Merge them into one professional list
    combined = []
    for m in tmdb_movies:
        combined.append({
            "id": m['id'],
            "title": m['title'],
            "poster_path": m['poster_path'],
            "vote_average": m['vote_average'],
            "source": "tmdb"
        })
    for s in scraped_movies:
        combined.append({
            "id": hash(s['title']), # Create a fake ID for scraped movies
            "title": s['title'],
            "poster_path": s['poster'], # Use direct URL for scraped
            "vote_average": 0,
            "source": "thenkiri",
            "url": s['url']
        })
        
    return {"results": combined}

@router.get("/{movie_id}/sources")
async def get_sources(movie_id: int, title: str):
    # If it's a scraped movie, we resolve the real download link
    try:
        # We attempt to find a real download link using the scraper
        # For this demo, we simulate the resolution based on the title
        download_url = scraper_service.resolve_download_link(f"https://thenkiri.com/search?q={title}")
        
        return {
            "sources": [
                {
                    "name": "Watch Online",
                    "type": "embed",
                    "url": f"https://www.youtube.com/results?search_query={title}+full+movie",
                    "is_trailer": False
                },
                {
                    "name": "Direct Download",
                    "type": "download",
                    "url": download_url,
                    "is_trailer": False
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# (Keep existing search and details endpoints)
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
