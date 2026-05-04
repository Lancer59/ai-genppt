"""SVG → PNG conversion using svglib + reportlab (pure Python, cross-platform)."""

import io
from pathlib import Path
from typing import Optional

from genppt.utils.logger import get_logger

logger = get_logger(__name__)


def svg_to_png(svg_path: Path, size: int = 64) -> Optional[bytes]:
    """
    Convert an SVG file to PNG bytes at the given square size.
    Returns None if conversion fails.
    """
    try:
        from reportlab.graphics import renderPM
        from svglib.svglib import svg2rlg

        drawing = svg2rlg(str(svg_path))
        if drawing is None:
            return None

        # Scale to target size
        scale_x = size / drawing.width if drawing.width else 1
        scale_y = size / drawing.height if drawing.height else 1
        drawing.width = size
        drawing.height = size
        drawing.transform = (scale_x, 0, 0, scale_y, 0, 0)

        buf = io.BytesIO()
        renderPM.drawToFile(drawing, buf, fmt="PNG")
        return buf.getvalue()

    except Exception as e:
        logger.warning(f"SVG→PNG conversion failed for {svg_path}: {e}")
        return None
