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
        results = tmdb_service.search_movies(query).get('results', [])
        # Normalize TMDB result to our internal Movie format
        return [
            {
                "id": res.get('id'),
                "title": res.get('title'),
                "overview": res.get('overview'),
                "poster_path": res.get('poster_path'),
                "backdrop_path": res.get('backdrop_path'),
                "release_date": res.get('release_date'),
                "vote_average": res.get('vote_average'),
                "url": None, # TMDB doesn't provide files
                "source": "tmdb"
            }
            for res in results
        ]

    def resolve_link(self, movie_id: str):
        return None

class ThenkiriProvider(BaseProvider):
    def search(self, query: str):
        # Use the scraper to find movies on thenkiri via their search page
        # We'll use a helper in ScraperService to handle the search
        results = scraper_service.search_movies(query)
        
        # Normalize Thenkiri results
        return [
            {
                "id": None, # Scraped movies might not have a TMDB ID immediately
                "title": res.get('title'),
                "overview": "Available on Thenkiri",
                "poster_path": None, # Scraper might not provide poster_path in a consistent format
                "backdrop_path": None,
                "release_date": None,
                "vote_average": None,
                "url": res.get('url'),
                "source": "thenkiri"
            }
            for res in results
        ]

    def resolve_link(self, movie_url: str):
        return scraper_service.resolve_direct_download(movie_url)

class ProviderOrchestrator:
    def __init__(self):
        self.providers = [TMDBProvider(), ThenkiriProvider()]

    async def universal_search(self, query: str):
        all_results = []
        for provider in self.providers:
            results = provider.search(query)
            all_results.extend(results)
        
        # Deduplicate based on title
        unique_results = {}
        for res in all_results:
            title = res.get('title', '').lower().strip()
            if not title: continue
            
            if title not in unique_results:
                unique_results[title] = res
            else:
                # If we already have a result for this title, 
                # prefer the one that has both metadata (TMDB) AND a link (Thenkiri)
                existing = unique_results[title]
                if existing.get('url') is None and res.get('url') is not None:
                    # Merge the link into the existing metadata-rich result
                    existing['url'] = res.get('url')
                    existing['source'] = "hybrid"
        
        return list(unique_results.values())

orchestrator = ProviderOrchestrator()
