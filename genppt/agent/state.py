from typing import Any, Dict, Optional

from typing_extensions import TypedDict

from genppt.llm.schemas import SlideOutline


class AgentState(TypedDict, total=False):
    """Shared state passed between all LangGraph nodes."""

    # ── Inputs ──────────────────────────────────────────────────────────────
    topic: str
    slide_count: int
    theme: str
    template_path: Optional[str]
    context: Optional[Dict[str, Any]]
    output_path: str

    # ── Computed by nodes ────────────────────────────────────────────────────
    outline: Optional[SlideOutline]
    image_paths: Optional[Dict[int, str]]   # slide_index -> local file path
    icon_paths: Optional[Dict[str, str]]    # icon_name   -> local png path
    pptx_path: Optional[str]
    error: Optional[str]
