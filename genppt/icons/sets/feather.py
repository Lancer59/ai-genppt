"""Feather Icons — MIT License — https://feathericons.com"""

from genppt.icons.cache import IconSetCache

FEATHER_ZIP = (
    "https://github.com/feathericons/feather/releases/download/v4.29.2/feather-sprite.zip"
)
# Feather release ZIP: icons/*.svg (flat)
_cache = IconSetCache("feather")


def ensure_downloaded() -> None:
    if not _cache.is_ready():
        _cache.download_zip(FEATHER_ZIP)


def find(name: str):
    ensure_downloaded()
    return _cache.find(name)
