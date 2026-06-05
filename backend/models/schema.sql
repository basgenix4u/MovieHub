-- Media Content Table
CREATE TABLE media_content (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER UNIQUE,
    title TEXT NOT NULL,
    type TEXT NOT NULL, -- 'movie', 'tv', 'video'
    release_year INTEGER,
    description TEXT,
    poster_url TEXT,
    backdrop_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Providers Table
CREATE TABLE providers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    base_url TEXT NOT NULL,
    priority INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true
);

-- Sources Table (The actual links)
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    media_id INTEGER REFERENCES media_content(id),
    provider_id INTEGER REFERENCES providers(id),
    url TEXT NOT NULL,
    type TEXT NOT NULL, -- 'stream', 'download'
    quality TEXT, -- '4K', '1080p', '720p'
    status TEXT DEFAULT 'active', -- 'active', 'dead'
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Activity Table
CREATE TABLE user_activity (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    media_id INTEGER REFERENCES media_content(id),
    action TEXT NOT NULL, -- 'watched', 'downloaded', 'favorite'
    progress INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
