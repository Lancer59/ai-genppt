"""
Icon resolver — searches across all icon sets (priority order) and
converts the best SVG match to a cached PNG for python-pptx embedding.

Priority:
  1. User's local icon dir (ICON_LOCAL_DIR)
  2. Tabler (largest set, ~5000 icons)
  3. Bootstrap Icons (~2000 icons)
  4. Heroicons (~300 icons)
  5. Feather (~300 icons)
  6. Simple Icons (brand logos)
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Optional

from genppt.config import settings
from genppt.icons.sets import bootstrap, feather, heroicons, simple_icons, tabler
from genppt.utils.logger import get_logger
from genppt.utils.svg_to_png import svg_to_png

logger = get_logger(__name__)

# Where resolved PNGs are cached
_PNG_CACHE: Path = settings.icon_cache_dir / "_png"
_PNG_CACHE.mkdir(parents=True, exist_ok=True)

# Ordered list of (label, find_fn) pairs
_SETS = [
    ("tabler", tabler.find),
    ("bootstrap", bootstrap.find),
    ("heroicons", heroicons.find),
    ("feather", feather.find),
    ("simple-icons", simple_icons.find),
]


def _find_in_local(name: str) -> Optional[Path]:
    """Search the user-supplied local icon directory first."""
    local_dir = settings.icon_local_dir
    if not local_dir or not local_dir.is_dir():
        return None
    name_lower = name.lower().replace("_", "-")
    for ext in (".png", ".svg"):
        p = local_dir / f"{name_lower}{ext}"
        if p.exists():
            return p
    # Fuzzy search
    for f in local_dir.iterdir():
        if name_lower in f.stem.lower() and f.suffix in (".png", ".svg"):
            return f
    return None


def _svg_path_to_png(svg_path: Path, name: str, size: int = 64) -> Optional[Path]:
    """Convert SVG to PNG and cache the result."""
    png_path = _PNG_CACHE / f"{name}_{size}.png"
    if png_path.exists():
        return png_path
    data = svg_to_png(svg_path, size=size)
    if data:
        png_path.write_bytes(data)
        return png_path
    return None


def resolve_one(name: str, size: int = 64) -> Optional[str]:
    """
    Resolve an icon name to a local PNG path.
    Checks local dir first, then all bundled icon sets.
    """
    name_norm = name.lower().replace("_", "-").strip()

    # 1. Local user directory (may already be PNG)
    local = _find_in_local(name_norm)
    if local:
        if local.suffix == ".png":
            return str(local)
        png = _svg_path_to_png(local, name_norm, size)
        if png:
            return str(png)

    # 2. Bundled icon sets in priority order
    for set_label, find_fn in _SETS:
        try:
            svg = find_fn(name_norm)
            if svg:
                png = _svg_path_to_png(svg, f"{set_label}-{name_norm}", size)
                if png:
                    logger.debug(f"Icon '{name}' resolved from {set_label}")
                    return str(png)
        except Exception as e:
            logger.warning(f"Icon set '{set_label}' error for '{name}': {e}")

    logger.warning(f"Icon '{name}' not found in any icon set")
    return None


async def _resolve_one_async(name: str) -> tuple[str, Optional[str]]:
    """Async wrapper so we can gather multiple resolutions."""
    loop = asyncio.get_event_loop()
    path = await loop.run_in_executor(None, resolve_one, name)
    return name, path


class IconResolver:
    async def resolve_many(self, names: List[str]) -> Dict[str, str]:
        """Resolve a list of icon names concurrently. Returns name→png_path dict."""
        if not names:
            return {}
        results = await asyncio.gather(
            *[_resolve_one_async(n) for n in names], return_exceptions=True
        )
        output: Dict[str, str] = {}
        for item in results:
            if isinstance(item, Exception):
                logger.warning(f"Icon resolution error: {item}")
                continue
            name, path = item
            if path:
                output[name] = path
        return output
