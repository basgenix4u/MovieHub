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
        self.search_url = "https://www.googleapis.com/youtube/v3/search"
        self.video_url = "https://www.googleapis.com/youtube/v3/videos"
        
        self.download_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }

    def search_full_movies(self, movie_title: str) -> List[Dict]:
        """
        ULTRA-FAST HYBRID INTELLIGENCE:
        Uses YouTube API for both Search AND Duration checks.
        Zero dependence on yt-dlp for discovery.
        """
        if not self.api_key:
            logger.info("No API key provided, using limited fallback.")
            return self._fast_scan_fallback(movie_title)

        try:
            # Step 1: Search for videos
            search_params = {
                'part': 'snippet',
                'q': f"{movie_title} full movie",
                'type': 'video',
                'videoDuration': 'long', # API filter for > 20 mins
                'maxResults': 10,
                'key': self.api_key
            }
            search_res = requests.get(self.search_url, params=search_params, timeout=5)
            if not search_res.ok:
                return self._fast_scan_fallback(movie_title)
                
            items = search_res.json().get('items', [])
            if not items:
                return []

            # Step 2: Get exact durations for these videos using the /videos endpoint
            # This is MUCH faster than yt-dlp
            video_ids = ",".join([item['id']['videoId'] for item in items])
            video_params = {
                'part': 'contentDetails',
                'id': video_ids,
                'key': self.api_key
            }
            video_res = requests.get(self.video_url, params=video_params, timeout=5)
            
            if video_res.ok:
                video_data = video_res.json().get('items', [])
                duration_map = {}
                for v in video_data:
                    # duration is in ISO 8601 format (e.g., PT1H30M10S)
                    duration_map[v['id']] = self._parse_iso8601_duration(v['contentDetails']['duration'])

                # Step 3: Filter and Return
                for item in items:
                    v_id = item['id']['videoId']
                    duration = duration_map.get(v_id, 0)
                    if duration >= 4800: # 80 minutes
                        return [{
                            "id": v_id,
                            "title": item['snippet']['title'],
                            "url": f"https://www.youtube.com/watch?v={v_id}",
                            "duration": duration,
                            "thumbnail": item['snippet']['thumbnails']['high']['url'],
                            "view_count": 0,
                            "upload_date": item['snippet']['publishedAt'],
                        }]
            
            return self._fast_scan_fallback(movie_title)

        except Exception as e:
            logger.error(f"Hybrid Search Error: {e}")
            return self._fast_scan_fallback(movie_title)

    def _parse_iso8601_duration(self, duration_str: str) -> int:
        """
        Converts ISO 8601 duration (PT#H#M#S) to total seconds.
        Example: PT1H30M10S -> 5410
        """
        import re
        seconds = 0
        hours = re.search(r'(\d+)H', duration_str)
        minutes = re.search(r'(\d+)M', duration_str)
        secs = re.search(r'(\d+)S', duration_str)
        
        if hours: seconds += int(hours.group(1)) * 3600
        if minutes: seconds += int(minutes.group(1)) * 60
        if secs: seconds += int(secs.group(1))
        return seconds

    def _fast_scan_fallback(self, movie_title: str) -> List[Dict]:
        # Very limited fallback to prevent hanging
        query = f"ytsearch3:{movie_title} full movie"
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' not in info: return []
                for entry in info['entries'][:3]:
                    try:
                        # Use a very fast check
                        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl_fast:
                            full_info = ydl_fast.extract_info(entry['url'], download=False)
                            if full_info.get('duration', 0) >= 4800:
                                return [{
                                    "id": entry['id'],
                                    "title": entry.get('title', 'Full Movie'),
                                    "url": entry.get('url'),
                                    "duration": full_info.get('duration', 0),
                                    "thumbnail": entry.get('thumbnail'),
                                    "view_count": 0,
                                    "upload_date": "",
                                }]
                    except: continue
        except: pass
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
