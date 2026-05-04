"""Themes package — exposes THEMES registry."""

from genppt.renderer.themes.base import Theme
from genppt.renderer.themes.corporate import CORPORATE
from genppt.renderer.themes.dark import DARK
from genppt.renderer.themes.minimalist import MINIMALIST

THEMES: dict[str, Theme] = {
    "dark": DARK,
    "corporate": CORPORATE,
    "minimalist": MINIMALIST,
}


def get_theme(name: str) -> Theme:
    theme = THEMES.get(name.lower())
    if not theme:
        available = ", ".join(THEMES)
        raise ValueError(f"Unknown theme '{name}'. Available: {available}")
    return theme
