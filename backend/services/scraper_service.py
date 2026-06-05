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
            for post in soup.select(".post-item, .movie-card, article, .entry-content a"):
                try:
                    link = post.get('href') if post.name == 'a' else post.select_one('a').get('href')
                    title = post.text.strip() if post.name == 'a' else post.select_one('h2, .title, a').text.strip()
                    
                    if link and title and len(title) > 2:
                        full_url = link if link.startswith('http') else f"https://thenkiri.com{link}"
                        movies.append({
                            "title": title,
                            "url": full_url,
                            "source": "thenkiri"
                        })
                except Exception:
                    continue
            return movies[:20]
        except Exception as e:
            print(f"Sync Error: {e}")
            return []

    def search_movies(self, query: str):
        """
        Performs a real search on thenkiri.com
        """
        search_url = f"https://thenkiri.com/?s={query}"
        try:
            response = requests.get(search_url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            movies = []
            # Search results usually follow a similar pattern to the home page posts
            for post in soup.select(".post-item, .movie-card, article, .entry-content a"):
                try:
                    link = post.get('href') if post.name == 'a' else post.select_one('a').get('href')
                    title = post.text.strip() if post.name == 'a' else post.select_one('h2, .title, a').text.strip()
                    
                    if link and title and len(title) > 2:
                        full_url = link if link.startswith('http') else f"https://thenkiri.com{link}"
                        movies.append({
                            "title": title,
                            "url": full_url,
                            "source": "thenkiri"
                        })
                except Exception:
                    continue
            return movies[:20]
        except Exception as e:
            print(f"Search Error: {e}")
            return []

    def resolve_direct_download(self, movie_url, depth=3):
        if depth == 0:
            return movie_url

        try:
            res = requests.get(movie_url, headers=self.headers, timeout=10)
            content_type = res.headers.get('Content-Type', '').lower()
            if 'video/' in content_type or 'application/octet-stream' in content_type:
                return movie_url

            soup = BeautifulSoup(res.text, 'lxml')
            
            best_link = None
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.text.lower()
                
                if any(ext in href.lower() for ext in ['.mp4', '.mkv', '.avi', '.mov']):
                    return href if href.startswith('http') else f"https://thenkiri.com{href}"
                
                if any(keyword in text or keyword in href.lower() for keyword in ['download', 'get-link', 'direct', 'mirror']):
                    best_link = href
                    break
            
            if best_link:
                full_best_link = best_link if best_link.startswith('http') else f"https://thenkiri.com{best_link}"
                return self.resolve_direct_download(full_best_link, depth - 1)
            
            return movie_url
        except Exception:
            return movie_url

scraper_service = ScraperService()
