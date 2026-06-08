import yt_dlp
import logging
from typing import List, Optional, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YouTubeExtractor")

class YouTubeExtractorService:
    def __init__(self):
        self.search_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True, 
        }
        
        self.download_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }

    def search_full_movies(self, movie_title: str) -> List[Dict]:
        """
        OPTIMIZED Intelligence Algorithm:
        Fast-tracking full movie discovery.
        """
        query = f"ytsearch10:{movie_title} full movie" # Reduced to 10 for speed
        
        try:
            with yt_dlp.YoutubeDL(self.search_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                
                if 'entries' not in info:
                    return []

                full_movies = []
                # LIMIT: Only check the top 5 most relevant videos to avoid timeouts
                candidates = info['entries'][:5]
                
                for entry in candidates:
                    try:
                        # Fast-check duration
                        full_info = ydl.extract_info(entry['url'], download=False)
                        duration = full_info.get('duration', 0)
                        
                        if duration >= 4800: # 80 minutes
                            full_movies.append({
                                "id": full_info.get('id'),
                                "title": full_info.get('title'),
                                "url": full_info.get('webpage_url'),
                                "duration": duration,
                                "thumbnail": full_info.get('thumbnail'),
                                "view_count": full_info.get('view_count'),
                                "upload_date": full_info.get('upload_date'),
                            })
                            # Once we find ONE high-quality full movie, we can return it 
                            # to ensure the UI responds instantly.
                            return full_movies 
                    except Exception as e:
                        logger.error(f"Error extracting metadata for {entry.get('url')}: {e}")
                        continue
                
                return full_movies

        except Exception as e:
            logger.error(f"YouTube Search Error: {e}")
            return []

    def get_direct_download_link(self, video_id: str) -> Optional[str]:
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(self.download_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('url')
        except Exception as e:
            logger.error(f"YouTube Extraction Error for {video_id}: {e}")
            return None

youtube_service = YouTubeExtractorService()
