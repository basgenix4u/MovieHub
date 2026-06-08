from abc import ABC, abstractmethod
from services.tmdb_service import tmdb_service

class BaseProvider(ABC):
    @abstractmethod
    def search(self, query: str):
        pass

    @abstractmethod
    def resolve_link(self, movie_id: str):
        pass

class TMDBProvider(BaseProvider):
    def search(self, query: str):
        results = tmdb_service.search_movies(query).get('results', [])
        return [
            {
                "id": res.get('id'),
                "title": res.get('title'),
                "overview": res.get('overview'),
                "poster_path": res.get('poster_path'),
                "backdrop_path": res.get('backdrop_path'),
                "release_date": res.get('release_date'),
                "vote_average": res.get('vote_average'),
                "url": None,
                "source": "tmdb"
            }
            for res in results
        ]

    def resolve_link(self, movie_id: str):
        return None

class ProviderOrchestrator:
    def __init__(self):
        # REMOVED ThenkiriProvider as per user request
        self.providers = [TMDBProvider()]

    async def universal_search(self, query: str):
        all_results = []
        for provider in self.providers:
            results = provider.search(query)
            all_results.extend(results)
        
        unique_results = {}
        for res in all_results:
            title = res.get('title', '').lower().strip()
            if not title: continue
            if title not in unique_results:
                unique_results[title] = res
        
        return list(unique_results.values())

orchestrator = ProviderOrchestrator()
