import yt_dlp
import logging
from typing import List, Optional, Dict

# Configure logging for high-end error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YouTubeExtractor")

class YouTubeExtractorService:
    def __init__(self):
        # yt-dlp options for searching and extracting
        self.search_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True, # Get metadata without downloading
        }
        
        self.download_opts = {
            'format': 'best[ext=mp4]/best', # Prioritize mp4 for direct device compatibility
            'quiet': True,
            'no_warnings': True,
        }

    def search_full_movies(self, movie_title: str) -> List[Dict]:
        """
        The 'Intelligence' Algorithm:
        Searches YouTube for the movie and filters for full-length versions.
        """
        # Construct a power-query for full movies
        query = f"ytsearch20:{movie_title} full movie complete film"
        
        try:
            with yt_dlp.YoutubeDL(self.search_opts) as ydl:
                # Search for videos
                info = ydl.extract_info(query, download=False)
                
                if 'entries' not in info:
                    return []

                full_movies = []
                for entry in info['entries']:
                    # We need the full metadata to check the duration
                    # extract_flat=True doesn't give duration, so we fetch it now
                    try:
                        full_info = ydl.extract_info(entry['url'], download=False)
                        duration = full_info.get('duration', 0)
                        
                        # Intelligence: Only accept videos longer than 80 minutes (4800 seconds)
                        if duration >= 4800:
                            full_movies.append({
                                "id": full_info.get('id'),
                                "title": full_info.get('title'),
                                "url": full_info.get('webpage_url'),
                                "duration": duration,
                                "thumbnail": full_info.get('thumbnail'),
                                "view_count": full_info.get('view_count'),
                                "upload_date": full_info.get('upload_date'),
                            })
                    except Exception as e:
                        logger.error(f"Error extracting metadata for {entry.get('url')}: {e}")
                        continue
                
                # Sort by view count (descending) to get the most reliable version
                full_movies.sort(key=lambda x: x.get('view_count', 0), reverse=True)
                return full_movies

        except Exception as e:
            logger.error(f"YouTube Search Error: {e}")
            return []

    def get_direct_download_link(self, video_id: str) -> Optional[str]:
        """
        The 'Extraction' Engine:
        Gets the raw .mp4 stream URL from YouTube.
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(self.download_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                # Return the direct URL to the video file
                return info.get('url')
        except Exception as e:
            logger.error(f"YouTube Extraction Error for {video_id}: {e}")
            return None

youtube_service = YouTubeExtractorService()
