from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup
from services.tmdb_service import tmdb_service
from services.scraper_service import scraper_service

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/proxy")
async def proxy_site(url: str):
    """
    Ghost Proxy: Fetches external site and serves it from our domain.
    Removes Ads and Headers to keep user in our UI.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Clean the HTML: Remove navigation, ads, and footers
        for tag in soup.select("nav, footer, .ads, .sidebar, script[src*='ads'], iframe[src*='ads']"):
            tag.decompose()
            
        # Fix links to be proxied (Advanced logic)
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('/'):
                a['href'] = f"https://moviehub-backend-wkgv.onrender.com/movies/proxy?url=https://thenkiri.com{a['href']}"
            elif 'thenkiri.com' in a['href']:
                a['href'] = f"https://moviehub-backend-wkgv.onrender.com/movies/proxy?url={a['href']}"

        return HTMLResponse(content=soup.prettify(), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy Error: {str(e)}")

@router.get("/download-link")
async def get_real_download(url: str):
    """Directly resolves to the .mp4/.mkv file"""
    final_url = scraper_service.resolve_direct_download(url)
    return {"download_url": final_url}

@router.get("/trending")
async def get_trending():
    # Mix TMDB and real Thenkiri data
    tmdb_movies = tmdb_service.get_trending_movies().get('results', [])
    scraped_movies = scraper_service.sync_latest_movies()
    
    combined = []
    for m in tmdb_movies:
        combined.append({
            "id": m['id'], "title": m['title'], "poster_path": m['poster_path'],
            "vote_average": m['vote_average'], "source": "tmdb"
        })
    for s in scraped_movies:
        combined.append({
            "id": hash(s['title']), "title": s['title'], "poster_path": s['poster'],
            "vote_average": 0, "source": "thenkiri", "url": s['url']
        })
    return {"results": combined}

@router.get("/{movie_id}")
async def get_movie(movie_id: int):
    try:
        return tmdb_service.get_movie_details(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}/sources")
async def get_sources(movie_id: int, title: str):
    # Intelligent routing to la real download/proxy
    return {
        "sources": [
            {
                "name": "Watch Online (Internal)",
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
