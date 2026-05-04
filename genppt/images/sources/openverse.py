from typing import Optional

import httpx


async def search_openverse(query: str, client: httpx.AsyncClient) -> Optional[str]:
    """
    Search Openverse (WordPress Foundation) for CC-licensed images.
    Returns a direct image URL or None.  No API key required for basic use.
    """
    try:
        resp = await client.get(
            "https://api.openverse.org/v1/images/",
            params={
                "q": query,
                "page_size": 5,
                "license_type": "commercial",
                "format": "json",
            },
            timeout=10.0,
            headers={"User-Agent": "ai-genppt/0.1 (open-source PPT generator)"},
        )
        data = resp.json()
        results = data.get("results", [])
        for r in results:
            url = r.get("url")
            if url:
                return url
    except Exception:
        pass
    return None
