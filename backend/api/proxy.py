from fastapi import APIRouter, HTTPException, Request, Response
import requests
from fastapi.responses import StreamingResponse
from typing import Optional

router = APIRouter(prefix="/proxy", tags=["Proxy"])

@router.get("/")
async def proxy_request(url: str):
    """
    Ghost Proxy: Fetches content from a target URL and strips headers 
    that prevent embedding (X-Frame-Options, CSP).
    """
    if not url:
        raise HTTPException(status_code=400, detail="Target URL is required")

    try:
        # Use a session to handle cookies and redirects
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://thenkiri.com/"
        })

        response = session.get(url, stream=True, timeout=15)
        
        # Prepare headers to strip restrictions
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection", "x-frame-options", "content-security-policy"]
        headers = {k: v for k, v in response.headers.items() if k.lower() not in excluded_headers}
        
        # Add headers to allow embedding
        headers["Access-Control-Allow-Origin"] = "*"
        headers["X-Frame-Options"] = "ALLOWALL" # Some browsers might ignore this, but it's better than DENY
        
        return StreamingResponse(
            response.iter_content(chunk_size=8192),
            status_code=response.status_code,
            headers=headers,
            media_type=response.headers.get("content-type")
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Proxy Error: {str(e)}")
