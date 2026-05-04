import hashlib
from pathlib import Path
from typing import Optional

from genppt.config import settings
from genppt.utils.logger import get_logger

logger = get_logger(__name__)


class ImageCache:
    def __init__(self) -> None:
        self.cache_dir = settings.image_cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()

    def get(self, url: str) -> Optional[Path]:
        for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            p = self.cache_dir / f"{self._key(url)}{ext}"
            if p.exists():
                return p
        return None

    def put(self, url: str, data: bytes, content_type: str = "image/jpeg") -> Path:
        ext_map = {
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif",
            "image/jpeg": ".jpg",
        }
        ext = ".jpg"
        for mime, e in ext_map.items():
            if mime in content_type:
                ext = e
                break
        path = self.cache_dir / f"{self._key(url)}{ext}"
        path.write_bytes(data)
        return path
