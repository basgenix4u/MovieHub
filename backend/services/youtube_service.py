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
        
        # Optimized download options to be more resilient to 404s/blocks
        self.download_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'youtube_include_dash_manifest': False,
        }

    def search_full_movies(self, movie_title: str) -> List[Dict]:
        if not self.api_key:
            return self._fast_scan_fallback(movie_title)

        try:
            search_params = {
                'part': 'snippet',
                'q': f"{movie_title} full movie",
                'type': 'video',
                'videoDuration': 'long',
                'maxResults': 10,
                'key': self.api_key
            }
            search_res = requests.get(self.search_url, params=search_params, timeout=5)
            if not search_res.ok:
                return self._fast_scan_fallback(movie_title)
                
            items = search_res.json().get('items', [])
            if not items:
                return []

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
                    duration_map[v['id']] = self._parse_iso8601_duration(v['contentDetails']['duration'])

                for item in items:
                    v_id = item['id']['videoId']
                    duration = duration_map.get(v_id, 0)
                    if duration >= 4800:
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
        query = f"ytsearch3:{movie_title} full movie"
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' not in info: return []
                for entry in info['entries'][:3]:
                    try:
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
        """
        FIXED Extraction Engine:
        Uses a more resilient approach to avoid 404s.
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            # We use a more aggressive format selection to ensure we get a direct URL
            opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                # Try to get the direct url from 'url' or 'formats'
                direct_url = info.get('url')
                if not direct_url and 'formats' in info:
                    # Find the best mp4 format that has a direct url
                    for f in info['formats']:
                        if f.get('ext') == 'mp4' and f.get('url'):
                            direct_url = f['url']
                            break
                return direct_url
        except Exception as e:
            logger.error(f"Extraction Error for {video_id}: {e}")
            return None

youtube_service = YouTubeExtractorService()
