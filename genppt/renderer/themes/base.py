"""Base theme dataclass — all themes inherit from this."""

from dataclasses import dataclass, field
from typing import Tuple

# Colour type: (R, G, B) each 0-255
RGB = Tuple[int, int, int]


@dataclass
class Theme:
    name: str

    # Backgrounds
    bg_color: RGB = (255, 255, 255)
    slide_bg: RGB = (255, 255, 255)          # fallback if no image

    # Text
    title_color: RGB = (30, 30, 30)
    body_color: RGB = (60, 60, 60)
    subtitle_color: RGB = (100, 100, 100)

    # Accents
    accent_color: RGB = (99, 102, 241)       # indigo-500
    accent_alt: RGB = (168, 85, 247)         # purple-500
    stat_color: RGB = (99, 102, 241)

    # Fonts (must be installed on the host system or fallback to Calibri)
    heading_font: str = "Segoe UI"
    body_font: str = "Segoe UI"

    # Sizes (in points)
    title_size: int = 40
    subtitle_size: int = 24
    body_size: int = 18
    notes_size: int = 12

    # Shape fill for section headers / accent bars
    accent_bar_height: float = 0.08         # fraction of slide height

    # Icon tint (used when coloring white icons on dark bg)
    icon_bg: RGB = (255, 255, 255)
