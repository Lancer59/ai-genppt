"""Heroicons — MIT License — https://heroicons.com"""

from genppt.icons.cache import IconSetCache

# Heroicons v2 release: contains optimized/24/outline/*.svg and optimized/24/solid/*.svg
HEROICONS_ZIP = (
    "https://github.com/tailwindlabs/heroicons/archive/refs/tags/v2.1.4.zip"
)

_cache = IconSetCache("heroicons")


def ensure_downloaded() -> None:
    if not _cache.is_ready():
        # Use outline variant (cleaner at small sizes)
        _cache.download_zip(HEROICONS_ZIP, svg_subpath_filter="optimized/24/outline")


def find(name: str):
    ensure_downloaded()
    return _cache.find(name)
