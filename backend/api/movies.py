from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
import requests
from services.tmdb_service import tmdb_service
from services.scraper_service import scraper_//service

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/proxy")
async def proxy_site(url: str):
    """
    The Ghost Proxy: Fetches content from target site and serves it from our server.
    This prevents 'X-Frame-Options: DENY' and keeps users in our UI.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # Clean the HTML to remove target site's navigation/ads (Basic version)
        soup = BeautifulSoup(response.text, 'lxml')
        for tag in soup.select("nav, footer, .ads, script[src*='ads']"):
            tag.decompose()
            
        return HTMLResponse(content=soup.prettify(), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy Error: {str(e)}")

@router.get("/download-link")
async def get_real_download(url: str):
    """Resolves the final direct file URL"""
    from services.scraper_service import scraper_service
    final_url = scraper_service.resolve_direct_download(url)
    return {"download_url": final_url}

@router.get("/trending")
async def get_trending():
    from services.scraper_service import scraper_service
    scraped = scraper_service.sync_latest_movies()
    return {"results": scraped}

@router.get("/{movie_id}")
async def get_movie(movie_id: int):
    try:
        return tmdb_service.get_movie_details(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}/sources")
async def get_sources(movie_id: int, title: str):
    from services.scraper_service import scraper_service
    # Intelligent resolution of sources
    return {
        "sources": [
            {
                "name": "Watch Online (Embedded)",
                "type": "embed",
                "url": f"https://moviehub-backend-wkgv.onrender.com/movies/proxy?url=https://thenkiri.com/search?q={title.replace(' ', '+')}",
                "is_trailer": False
            },
            {
                "name": "Direct Download",
                "type": "download",
                "url": f"https://moviehub-backend-wkgv.onrender.com/movies/download-link?url=https://thenkiri.com/search?q={title.replace(' ', '+')}",
                "is_trailer": False
            }
        ]
    }
