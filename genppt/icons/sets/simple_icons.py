"""Simple Icons — CC0 License — https://simpleicons.org (brand logos)"""

from genppt.icons.cache import IconSetCache

SIMPLE_ICONS_ZIP = (
    "https://github.com/simple-icons/simple-icons/archive/refs/tags/12.3.0.zip"
)

_cache = IconSetCache("simple-icons")


def ensure_downloaded() -> None:
    if not _cache.is_ready():
        _cache.download_zip(SIMPLE_ICONS_ZIP, svg_subpath_filter="icons/")


def find(name: str):
    ensure_downloaded()
    return _cache.find(name)
