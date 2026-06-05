from abc import ABC, abstractmethod
from services.tmdb_service import tmdb_service
from services.scraper_service import scraper_service

class BaseProvider(ABC):
    @abstractmethod
    def search(self, query: str):
        pass

    @abstractmethod
    def resolve_link(self, movie_id: str):
        pass

class TMDBProvider(BaseProvider):
    def search(self, query: str):
        return tmdb_service.search_movies(query).get('results', [])

    def resolve_link(self, movie_id: str):
        return None # TMDB provides metadata, not files

class ThenkiriProvider(BaseProvider):
    def search(self, query: str):
        # Use the scraper to find movies on thenkiri
        return scraper_service.sync_latest_movies() # Simplified for now

    def resolve_link(self, movie_url: str):
        return scraper_//service.resolve_direct_download(movie_url)

class ProviderOrchestrator:
    def __init__(self):
        self.providers = [TMDBProvider(), ThenkiriProvider()]

    async def universal_search(self, query: str):
        all_results = []
        for provider in self.providers:
            results = provider.search(query)
            all_results.extend(results)
        
        # Deduplicate and Rank (Simple logic for now)
        unique_results = {}
        for res in all_results:
            title = res.get('title').lower()
            if title not in unique_results:
                unique_results[title] = res
        
        return list(unique_results.values())

orchestrator = ProviderOrchestrator()
