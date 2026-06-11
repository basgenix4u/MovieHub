import yt_dlp
import requests
import logging
from typing import List, Optional, Dict, Tuple
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
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
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

    def get_direct_download_data(self, video_id: str) -> Optional[Tuple[str, Dict]]:
        """
        ULTRA-ROBUST EXTRACTION:
        Attempts to find any playable single-file stream, handling age-restricted 
        and DASH-only videos by iterating through all available formats.
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Use more aggressive extraction options to bypass some restrictions
            extract_opts = {
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'user_agent': self.download_opts['user_agent'],
                # Try different clients to potentially bypass age restrictions
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            }

            with yt_dlp.YoutubeDL(extract_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    logger.error(f"yt-dlp failed to extract info for {video_id}")
                    return None

                # Priority 1: Combined MP4 (Best Quality)
                formats = info.get('formats', [])
                combined_mp4 = [
                    f for f in formats 
                    if f.get('ext') == 'mp4' and f.get('vcodec') != 'none' and f.get('acodec') != 'none'
                ]
                if combined_mp4:
                    best_f = max(combined_mp4, key=lambda x: x.get('height', 0))
                    return best_f.get('url'), self._get_headers()

                # Priority 2: Any combined format (MKV, WebM etc)
                combined_any = [
                    f for f in formats 
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none'
                ]
                if combined_any:
                    best_f = max(combined_any, key=lambda x: x.get('height', 0))
                    return best_f.get('url'), self._get_headers()

                # Priority 3: Fallback to the main URL provided by yt-dlp (if combined)
                if info.get('url'):
                    # Note: this is often just a video-only or audio-only stream in DASH
                    # but it's our last resort.
                    return info['url'], self._get_headers()

                logger.error(f"No playable combined stream found for {video_id}. Video may be age-restricted or DASH-only.")
                return None
        except Exception as e:
            logger.error(f"Extraction Error for {video_id}: {e}")
            return None

    def _get_headers(self) -> Dict:
        return {
            "User-Agent": self.download_opts['user_agent'],
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.youtube.com/",
        }

youtube_service = YouTubeExtractorService()
