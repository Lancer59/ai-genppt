import asyncio

from genppt.agent.state import AgentState
from genppt.images.fetcher import ImageFetcher
from genppt.icons.resolver import IconResolver
from genppt.llm.client import get_llm
from genppt.llm.schemas import SlideOutline
from genppt.renderer.builder import PresentationBuilder
from genppt.utils.logger import get_logger

logger = get_logger(__name__)

# ── Prompt template ──────────────────────────────────────────────────────────
_PLAN_PROMPT = """\
You are a professional presentation designer and expert copywriter.
Create a compelling, well-structured presentation on the following topic.

Topic: {topic}
Number of slides: {slide_count}
Preferred theme: {theme}
{context_block}

Guidelines:
- Slide 1 must always be a "title" layout.
- Last slide must always be a "closing" layout.
- Use a variety of layout types for visual interest (content, two_column, stats_callout, full_bleed_image, section_header).
- For every slide, suggest a concise image_query (3–6 words) for photo search — even for title/closing.
- Suggest 1–3 icon names per slide using kebab-case names common in Bootstrap Icons / Feather Icons
  (e.g. "rocket", "bar-chart", "shield-check", "users", "lightning-charge", "globe").
- Keep bullet points concise: max 8 words each, max 5 bullets per slide.
- For stats_callout slides, provide exactly 2–4 StatItem entries with impactful numbers.
- For two_column slides, fill both left_bullets and right_bullets.
- Write detailed, natural-sounding speaker notes (2–4 sentences) for every slide.
- The presentation_title should be punchy and professional.
"""


def plan_slides(state: AgentState) -> AgentState:
    """Node 1 — LLM generates a structured SlideOutline."""
    llm = get_llm(temperature=1)
    structured_llm = llm.with_structured_output(SlideOutline)

    context_block = ""
    if state.get("context"):
        ctx = state["context"]
        lines = [f"  {k}: {v}" for k, v in ctx.items()]
        context_block = "Context:\n" + "\n".join(lines)

    prompt = _PLAN_PROMPT.format(
        topic=state["topic"],
        slide_count=state.get("slide_count", 10),
        theme=state.get("theme", "dark"),
        context_block=context_block,
    )

    logger.info("Calling LLM to plan slides...")
    outline: SlideOutline = structured_llm.invoke(prompt)
    logger.info(f"LLM planned {len(outline.slides)} slides")
    return {**state, "outline": outline}


# ── Asset fetching ─────────────────────────────────────────────────────────
async def _fetch_all_assets(
    outline: SlideOutline,
) -> tuple[dict[int, str], dict[str, str]]:
    """Run image fetching and icon resolution concurrently."""
    fetcher = ImageFetcher()
    resolver = IconResolver()

    image_queries: dict[int, str] = {}
    icon_names: set[str] = set()

    for i, slide in enumerate(outline.slides):
        if slide.image_query:
            image_queries[i] = slide.image_query
        if slide.icon_names:
            icon_names.update(slide.icon_names)

    image_task = fetcher.fetch_many(image_queries)
    icon_task = resolver.resolve_many(list(icon_names))

    image_paths, icon_paths = await asyncio.gather(image_task, icon_task)
    return image_paths, icon_paths


def fetch_assets(state: AgentState) -> AgentState:
    """Node 2 — Fetch images + icons concurrently (asyncio.gather inside)."""
    outline = state["outline"]
    logger.info("Fetching images and icons...")
    image_paths, icon_paths = asyncio.run(_fetch_all_assets(outline))
    logger.info(
        f"Fetched {len(image_paths)} images, resolved {len(icon_paths)} icons"
    )
    return {**state, "image_paths": image_paths, "icon_paths": icon_paths}


def build_pptx(state: AgentState) -> AgentState:
    """Node 3 — Assemble the .pptx file using python-pptx."""
    builder = PresentationBuilder(
        theme_name=state.get("theme", "dark"),
        template_path=state.get("template_path"),
    )

    output_path = state.get("output_path", "output/presentation.pptx")
    logger.info(f"Building PPTX -> {output_path}")

    pptx_path = builder.build(
        outline=state["outline"],
        image_paths=state.get("image_paths") or {},
        icon_paths=state.get("icon_paths") or {},
        output_path=output_path,
    )
    return {**state, "pptx_path": pptx_path}
