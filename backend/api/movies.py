from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
import requests
from services.tmdb_service import tmdb_service
from services.scraper_service import scraper_service

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

@router.get("/{movie_id}/sources")
async def get_sources(movie_id: int, title: str):
    try:
        return tmdb_service.get_external_sources(movie_id, title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/proxy")
async def proxy_site(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        for tag in soup.select("nav, footer, .ads, script[src*='ads']"):
            tag.decompose()
            
        return HTMLResponse(content=soup.prettify(), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy Error: {str(e)}")

@router.get("/download-link")
async def get_real_download(url: str):
    from services.scraper_service import scraper_service
    final_url = scraper_service.resolve_direct_download(url)
    return {"download_url": final_url}
