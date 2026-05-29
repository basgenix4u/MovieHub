import requests
from core.config import settings

class TMDBService:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_trending_movies(self):
        return self._get("/trending/movie/day")

    def search_movies(self, query: str):
        return self._get("/search/movie", params={"query": query})

    def get_movie_details(self, movie_id: int):
        return self._get(f"/movie/{movie_id}", params={"append_to_response": "videos,credits"})

tmdb_service = TMDBService()
