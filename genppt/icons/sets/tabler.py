"""Tabler Icons — MIT License — https://tabler.io/icons"""

from genppt.icons.cache import IconSetCache

TABLER_ZIP = (
    "https://github.com/tabler/tabler-icons/releases/download/v3.7.0/tabler-icons-3.7.0.zip"
)

_cache = IconSetCache("tabler")


def ensure_downloaded() -> None:
    if not _cache.is_ready():
        # Tabler ZIP: svg/outline/*.svg
        _cache.download_zip(TABLER_ZIP, svg_subpath_filter="svg/outline")


def find(name: str):
    ensure_downloaded()
    return _cache.find(name)
