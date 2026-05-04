from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class StatItem(BaseModel):
    """A single statistic for stats_callout slides."""

    value: str = Field(description="The stat value, e.g. '98%' or '$4.2B'")
    label: str = Field(description="Short label below the stat, e.g. 'Customer Satisfaction'")


class SlideSpec(BaseModel):
    """Specification for a single slide."""

    layout: Literal[
        "title",
        "section_header",
        "content",
        "two_column",
        "full_bleed_image",
        "stats_callout",
        "closing",
    ] = Field(description="Slide layout type")

    title: str = Field(description="Slide title or headline")
    subtitle: Optional[str] = Field(default=None, description="Subtitle (title/closing slides)")
    bullets: Optional[List[str]] = Field(
        default=None, description="Bullet points for content slides (max 5, concise)"
    )
    image_query: Optional[str] = Field(
        default=None,
        description="Search query to find a relevant photo, e.g. 'modern hospital technology'",
    )
    icon_names: Optional[List[str]] = Field(
        default=None,
        description=(
            "1-3 icon names from standard sets, e.g. ['rocket', 'bar-chart', 'users']. "
            "Use kebab-case names common across Bootstrap/Feather/Heroicons."
        ),
    )
    # Two-column layout
    left_title: Optional[str] = Field(default=None, description="Left column heading")
    left_bullets: Optional[List[str]] = Field(default=None, description="Left column bullets")
    right_title: Optional[str] = Field(default=None, description="Right column heading")
    right_bullets: Optional[List[str]] = Field(default=None, description="Right column bullets")

    # Stats callout layout
    stats: Optional[List[StatItem]] = Field(
        default=None, description="2–4 stat items for stats_callout layout"
    )

    speaker_notes: str = Field(default="", description="Detailed speaker notes for this slide")


class SlideOutline(BaseModel):
    """Full presentation outline produced by the LLM."""

    presentation_title: str = Field(description="The overall presentation title")
    theme: str = Field(default="dark", description="Theme name: dark | corporate | minimalist")
    total_slides: int = Field(description="Number of slides in this outline")
    slides: List[SlideSpec] = Field(description="Ordered list of slide specifications")
