import requests
from core.config import settings

class TMDBService:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.token = settings.TMDB_READ_ACCESS_TOKEN
        self.base_url = settings.TMDB_BASE_URL

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json"
        }
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_trending_movies(self):
        return self._get("/trending/movie/day")

    def search_movies(self, query: str):
        return self._get("/search/movie", params={"query": query})

    def get_movie_details(self, movie_id: int):
        return self._get(f"/movie/{movie_id}", params={"append_to_response": "videos,credits"})

    def get_recommendations(self, movie_id: int):
        return self._get(f"/movie/{movie_id}/recommendations")

    def get_external_sources(self, movie_id: int, title: str):
        # This is a simulated source aggregator. 
        # In a real app, this would scrape or use API endpoints from other sites.
        return {
            "sources": [
                {
                    "name": "YouTube",
                    "type": "embed",
                    "url": f"https://www.youtube.com/results?search_query={title}+full+movie",
                    "is_trailer": False
                },
                {
                    "name": "Nkiri",
                    "type": "external",
                    "url": f"https://nkiri.com/search?q={title.replace(' ', '+')}",
                    "is_trailer": False
                },
                {
                    "name": "Download Center",
                    "type": "download",
                    "url": f"https://www.google.com/search?q=download+{title.replace(' ', '+')}+movie",
                    "is_trailer": False
                }
            ]
        }

tmdb_service = TMDBService()
