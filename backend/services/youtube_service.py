import yt_dlp
import requests
import logging
from typing import List, Optional, Dict
from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YouTubeExtractor")

class YouTubeExtractorService:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        
        self.download_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }

    def search_full_movies(self, movie_title: str) -> List[Dict]:
        """
        HYBRID INTELLIGENCE ALGORITHM:
        Tries Official API first for instant filtering, falls back to Fast-Scan.
        """
        # Strategy 1: Official API (Instant and Accurate)
        if self.api_key:
            try:
                params = {
                    'part': 'snippet',
                    'q': f"{movie_title} full movie complete film",
                    'type': 'video',
                    'videoDuration': 'long', # Only videos longer than 20 minutes
                    'maxResults': 10,
                    'key': self.api_key
                }
                res = requests.get(self.base_url, params=params, timeout=5)
                if res.ok:
                    data = res.json()
                    results = []
                    for item in data.get('items', []):
                        # The API doesn't give exact duration in the search endpoint, 
                        # so we verify the top match using yt-dlp
                        video_id = item['id']['videoId']
                        duration = self._get_duration(video_id)
                        if duration >= 4800: # 80 mins
                            results.append({
                                "id": video_id,
                                "title": item['snippet']['title'],
                                "url": f"https://www.youtube.com/watch?v={video_id}",
                                "duration": duration,
                                "thumbnail": item['snippet']['thumbnails']['high']['url'],
                                "view_count": 0, # API search doesn't provide this
                                "upload_date": item['snippet']['publishedAt'],
                            })
                            return results # Found a winner instantly!
                logger.info("API search failed or no full movie found, switching to fallback.")
            except Exception as e:
                logger.error(f"API Error: {e}")

        # Strategy 2: Fast-Scan Fallback (Limited to top 3 to prevent hanging)
        return self._fast_scan_fallback(movie_title)

    def _get_duration(self, video_id: str) -> int:
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('duration', 0)
        except:
            return 0

    def _fast_scan_fallback(self, movie_title: str) -> List[Dict]:
        query = f"ytsearch5:{movie_title} full movie"
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' not in info: return []
                
                for entry in info['entries'][:3]: # Only check top 3 to avoid timeout
                    duration = self._get_duration(entry['id'])
                    if duration >= 4800:
                        return [{
                            "id": entry['id'],
                            "title": entry.get('title', 'Full Movie'),
                            "url": entry.get('url'),
                            "duration": duration,
                            "thumbnail": entry.get('thumbnail'),
                            "view_count": 0,
                            "upload_date": "",
                        }]
        except Exception as e:
            logger.error(f"Fallback Error: {e}")
        return []

    def get_direct_download_link(self, video_id: str) -> Optional[str]:
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(self.download_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('url')
        except Exception as e:
            logger.error(f"Extraction Error: {e}")
            return None

youtube_service = YouTubeExtractorService()
