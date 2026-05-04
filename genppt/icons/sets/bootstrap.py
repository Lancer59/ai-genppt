"""Bootstrap Icons — MIT License — https://icons.getbootstrap.com"""

from genppt.icons.cache import IconSetCache

# Latest release ZIP: contains icons/*.svg
BOOTSTRAP_ZIP = (
    "https://github.com/twbs/icons/releases/download/v1.11.3/bootstrap-icons-1.11.3.zip"
)

_cache = IconSetCache("bootstrap")


def ensure_downloaded() -> None:
    if not _cache.is_ready():
        _cache.download_zip(BOOTSTRAP_ZIP, svg_subpath_filter="bootstrap-icons")


def find(name: str):
    ensure_downloaded()
    return _cache.find(name)
