import requests
from bs4 import BeautifulSoup
from core.config import settings
import re

class ScraperService:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://thenkiri.com/"
        }

    def sync_latest_movies(self):
        url = "https://thenkiri.com/"
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            movies = []
            # Target Thenkiri's specific movie post structure
            for post in soup.select(".post-item, .movie-card, article, .entry-content a"):
                link = post.get('href') if post.name == 'a' else post.select_one('a').get('href')
                title = post.text.strip() if post.name == 'a' else post.select_one('h2, .title, a').text.strip()
                
                if link and title and len(title) > 2:
                    full_url = link if link.startswith('http') else f"https://thenkiri.com{link}"
                    movies.append({
                        "title": title,
                        "url": full_url,
                        "source": "thenkiri"
                    })
            return movies[:20] # Return top 20
        except Exception as e:
            print(f"Sync Error: {e}")
            return []

    def resolve_direct_download(self, movie_url):
        """
        Deep Link Resolver:
        Follows the path: Movie Page -> Download Page -> Direct File.
        """
        try:
            # Step 1: Visit movie page to find the download button
            res = requests.get(movie_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            
            download_page = None
            for a in soup.find_all('a', href=True):
                if 'download' in a.text.lower() or 'download' in a['href'].lower():
                    download_page = a['href']
                    break
            
            if not download_page: return movie_url

            if not download_page.startswith('http'):
                download_page = f"https://thenkiri.com{download_page}"
                
            # Step 2: Visit the download page to find the actual file (.mp4, .mkv)
            res_final = requests.get(download_page, headers=self.headers, timeout=10)
            soup_final = BeautifulSoup(res_final.text, 'lxml')
            
            for a in soup_final.find_all('a', href=True):
                href = a['href']
                if any(ext in href.lower() for ext in ['.mp4', '.mkv', '.avi', '.mov']):
                    return href # Found the real file!
            
            return download_page
        except Exception:
            return movie_url

scraper_service = ScraperService()
