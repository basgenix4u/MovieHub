import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "MovieHub"
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY", "your_api_key_here")
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/moviehub")

settings = Settings()
