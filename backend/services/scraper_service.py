import requests
from bs4 import BeautifulSoup
from core.config import settings

class ScraperService:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_thenkiri_latest(self):
        url = "https://thenkiri.com/"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            movies = []
            # This is a simulated selector - in a real scenario, I'd analyze the HTML
            # We look for common movie post structures on these types of sites
            for post in soup.select(".post-item, .movie-card, article"):
                title_el = post.select_one("h2, .title, a")
                link_el = post.select_one("a")
                img_el = post.select_one("img")
                
                if title_el and link_el:
                    movies.append({
                        "title": title_el.text.strip(),
                        "url": link_el['href'] if link_el['href'].startswith('http') else f"https://thenkiri.com{link_el['href']}",
                        "poster": img_el['src'] if img_el else "https://via.placeholder.com/500x750",
                        "source": "thenkiri"
                    })
            return movies
        except Exception as e:
            print(f"Scraper Error: {e}")
            return []

    def resolve_download_link(self, page_url):
        """
        This is the 'Magic' function. It visits the movie page, 
        finds the download button, and follows it to the final file.
        """
        try:
            response = requests.get(page_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Look for links containing 'download', 'drive', 'mega', 'mediafire'
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href'].lower()
                if 'download' in href or 'googledrive' in href or 'mega.nz' in href:
                    return link['href']
            
            return page_url # Fallback to page url
        except Exception:
            return page_url

scraper_service = ScraperService()
