from typing import Optional

import httpx


async def search_wikimedia(query: str, client: httpx.AsyncClient) -> Optional[str]:
    """
    Search Wikimedia Commons for a bitmap image matching the query.
    Returns a direct image URL or None.  No API key required.
    """
    try:
        resp = await client.get(
            "https://commons.wikimedia.org/w/api.php",
            params={
                "action": "query",
                "generator": "search",
                "gsrnamespace": 6,          # File namespace
                "gsrsearch": f"filetype:bitmap {query}",
                "gsrlimit": 5,
                "prop": "imageinfo",
                "iiprop": "url|size|mime",
                "iiurlwidth": 1920,
                "format": "json",
            },
            timeout=10.0,
        )
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            info_list = page.get("imageinfo", [])
            if not info_list:
                continue
            info = info_list[0]
            mime = info.get("mime", "")
            if not mime.startswith("image/"):
                continue
            url = info.get("thumburl") or info.get("url")
            if url:
                return url
    except Exception:
        pass
    return None
