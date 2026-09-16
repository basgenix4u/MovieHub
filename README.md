<div align="center">

# 🎬 MovieHub

**A premium cinema-grade streaming discovery platform — browse, watch trailers, and curate your personal watchlist.**

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

</div>

---

## ✨ Overview

MovieHub is a full-stack movie discovery experience built around the **TMDB** catalogue. It pairs a polished, dark-themed Next.js front end with a FastAPI service that proxies TMDB, resolves YouTube trailers, and persists user data — all behind Supabase authentication.

Browse trending titles, search the full TMDB archive, open a title to watch its trailer inline, save favourites, and build a watchlist that follows you across devices.

---

## 🚀 Features

### Discovery
- **Trending rail** — daily and weekly trending titles on the home screen
- **Full-text search** — query the entire TMDB catalogue with instant results
- **Rich detail pages** — synopsis, cast, ratings, runtime, and related titles
- **Infinite browse** — category pages with smooth pagination

### Playback
- **Inline trailer player** — YouTube trailers resolved server-side and played in a modal
- **Watch route** — dedicated full-bleed viewing experience
- **Age-restricted gating** — mature titles require confirmation before playback

### Personal
- **Supabase auth** — email + OAuth sign-in with persistent sessions
- **Favourites** — one-tap heart on any title, synced to your account
- **Watchlist** — curate what to watch next from any device
- **Profile page** — view and manage your saved titles

### Engineering
- **Server-side TMDB proxy** — API keys never reach the browser
- **Type-safe data layer** — shared TypeScript models across routes
- **Responsive by default** — mobile-first layouts that scale to desktop

---

## 🛠 Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 15 (App Router), React, TypeScript |
| Styling | Tailwind CSS, custom cinema theme |
| Backend | Python, FastAPI, Uvicorn |
| Database & Auth | Supabase (Postgres + GoTrue) |
| Media Data | TMDB API, YouTube Data API |
| Icons | Lucide |
| Deployment | Vercel (frontend) · Render (backend) |

---

## ⚡ Quick Start

### Prerequisites
- **Node.js** 20+
- **Python** 3.11+
- A **TMDB** account (free API key)
- A **Supabase** project

### 1. Frontend

```bash
npm install
npm run dev
# → http://localhost:3000
```

### 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# → http://localhost:8000/docs
```

---

## 🔐 Environment Variables

Create `.env.local` in the project root:

```env
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Create `backend/.env` for the API service:

```env
TMDB_API_KEY=<your-tmdb-key>
TMDB_READ_ACCESS_TOKEN=<your-tmdb-read-token>
YOUTUBE_API_KEY=<your-youtube-key>
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<database>
```

> ⚠️ **Never commit real credentials.** Every secret above is loaded from the environment — the app fails closed rather than falling back to insecure defaults.

Generate strong secrets with:

```bash
openssl rand -base64 32
```

---

## 📁 Project Structure

```text
MovieHub/
├── src/
│   ├── app/
│   │   ├── page.tsx            # Home — trending + hero
│   │   ├── movie/[id]/         # Title detail view
│   │   ├── watch/              # Full-bleed playback
│   │   ├── search/             # Catalogue search
│   │   ├── trending/           # Trending grid
│   │   ├── watchlist/          # Saved titles
│   │   └── profile/            # Account management
│   ├── components/             # Navbar, MovieCard, TrailerModal, …
│   ├── context/                # AuthContext provider
│   └── lib/                    # API + Supabase clients
├── backend/
│   ├── api/                    # movies, favorites, proxy routes
│   ├── core/                   # settings, database
│   ├── models/                 # Pydantic schemas
│   ├── services/               # TMDB / YouTube integrations
│   └── main.py                 # FastAPI entrypoint
└── docs/DEPLOYMENT.md
```

---

## 📜 Available Scripts

| Command | Description |
| --- | --- |
| `npm run dev` | Start the dev server with hot reload |
| `npm run build` | Production build |
| `npm run start` | Serve the production build |
| `npm run lint` | Run ESLint |

---

## 🌐 Deployment

Detailed instructions live in [`docs/DEPLOYMENT.md`](./docs/DEPLOYMENT.md).

- **Frontend** → Vercel (set the three `NEXT_PUBLIC_*` variables)
- **Backend** → Render or Railway (the included `Procfile` and `runtime.txt` are pre-configured)

---

## 🤝 Contributing

Issues and pull requests are welcome. Please open an issue to discuss substantial changes first.

---

## 📄 License

Released under the [MIT License](./LICENSE).

---

<div align="center">

Built by [Abdulbasit Abdulalim](https://github.com/basgenix4u)

Movie data courtesy of [TMDB](https://www.themoviedb.org) — this product uses the TMDB API but is not endorsed or certified by TMDB.

</div>
