"""
Icon set cache — downloads ZIP releases from GitHub on first use,
extracts SVGs, and builds a name→path index for fast lookup.
"""

import io
import zipfile
from pathlib import Path
from typing import Dict, Optional

import httpx

from genppt.config import settings
from genppt.utils.logger import get_logger

logger = get_logger(__name__)


class IconSetCache:
    def __init__(self, set_name: str) -> None:
        self.set_name = set_name
        self.cache_dir: Path = settings.icon_cache_dir / set_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._index: Dict[str, Path] = {}

    def is_ready(self) -> bool:
        return any(self.cache_dir.glob("*.svg"))

    def download_zip(self, url: str, svg_subpath_filter: str = "") -> bool:
        """
        Download a ZIP from `url`, extract all SVG files whose path contains
        `svg_subpath_filter` (empty = all SVGs), flatten into cache_dir.
        """
        logger.info(f"[{self.set_name}] Downloading icon set from {url} …")
        try:
            with httpx.Client(timeout=120.0, follow_redirects=True) as client:
                resp = client.get(url)
                resp.raise_for_status()

            count = 0
            with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
                for name in zf.namelist():
                    if not name.endswith(".svg"):
                        continue
                    if svg_subpath_filter and svg_subpath_filter not in name:
                        continue
                    stem = Path(name).stem.lower().replace("_", "-")
                    data = zf.read(name)
                    (self.cache_dir / f"{stem}.svg").write_bytes(data)
                    count += 1

            logger.info(f"[{self.set_name}] Extracted {count} SVG icons")
            return True
        except Exception as e:
            logger.warning(f"[{self.set_name}] Download failed: {e}")
            return False

    def build_index(self) -> Dict[str, Path]:
        self._index = {p.stem: p for p in self.cache_dir.glob("*.svg")}
        return self._index

    def find(self, name: str) -> Optional[Path]:
        if not self._index:
            self.build_index()
        name = name.lower().replace("_", "-")
        # 1. Exact match
        if name in self._index:
            return self._index[name]
        # 2. Starts-with match
        for key, path in self._index.items():
            if key.startswith(name):
                return path
        # 3. Contains match
        for key, path in self._index.items():
            if name in key:
                return path
        return None
