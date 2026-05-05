import asyncio
from pathlib import Path
from typing import Dict, List, Optional

import httpx

from genppt.config import settings
from genppt.images.cache import ImageCache
from genppt.images.sources.openverse import search_openverse
from genppt.images.sources.picsum import get_picsum_url
from genppt.images.sources.wikimedia import search_wikimedia
from genppt.utils.logger import get_logger

logger = get_logger(__name__)
_cache = ImageCache()


class ImageFetcher:
    """
    Multi-source image fetcher.
    Tries Wikimedia → Openverse in parallel, then falls back to Picsum.
    All results are cached locally.
    """

    async def _download(self, url: str, client: httpx.AsyncClient) -> Optional[Path]:
        cached = _cache.get(url)
        if cached:
            return cached
        try:
            resp = await client.get(url, timeout=15.0, follow_redirects=True)
            if resp.status_code == 200:
                ct = resp.headers.get("content-type", "image/jpeg")
                return _cache.put(url, resp.content, ct)
        except Exception as e:
            logger.warning(f"Download failed ({url}): {e}")
        return None

    async def fetch_one(self, query: str, client: httpx.AsyncClient) -> Optional[Path]:
        """Try all enabled sources; return the first successful local path."""
        source_coroutines = []
        if settings.image_source_wikimedia:
            source_coroutines.append(search_wikimedia(query, client))
        if settings.image_source_openverse:
            source_coroutines.append(search_openverse(query, client))

        if source_coroutines:
            urls: List = await asyncio.gather(*source_coroutines, return_exceptions=True)
            for url in urls:
                if isinstance(url, str) and url:
                    path = await self._download(url, client)
                    if path:
                        return path

        # Picsum fallback — always succeeds
        if settings.image_source_picsum:
            fallback_url = get_picsum_url(query)
            return await self._download(fallback_url, client)

        return None

    async def fetch_many(self, queries: Dict[int, str]) -> Dict[int, str]:
        """Fetch images for multiple slide indices concurrently."""
        if not queries:
            return {}

        async with httpx.AsyncClient(
            headers={"User-Agent": "ai-genppt/0.1 (open-source PPT generator)"}
        ) as client:
            tasks = {idx: self.fetch_one(q, client) for idx, q in queries.items()}
            results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        output: Dict[int, str] = {}
        for idx, result in zip(tasks.keys(), results):
            if isinstance(result, Path):
                output[idx] = str(result)
            elif isinstance(result, Exception):
                logger.warning(f"Image fetch error slide {idx}: {result}")
        return output
