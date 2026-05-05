from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CACHE_DIR = Path.home() / ".ai-genppt" / "cache"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── Azure OpenAI ────────────────────────────────────────────────────────
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment_name: Optional[str] = "gpt-5.3-chat"
    azure_openai_api_version: str = "2024-08-01-preview"

    # ── Generic OpenAI-compatible ───────────────────────────────────────────
    openai_base_url: Optional[str] = None
    openai_api_key: Optional[str] = None

    # ── Image sources ───────────────────────────────────────────────────────
    image_source_wikimedia: bool = True
    image_source_openverse: bool = True
    image_source_picsum: bool = True

    # ── Icons ───────────────────────────────────────────────────────────────
    icon_local_dir: Optional[Path] = None

    # ── Output ──────────────────────────────────────────────────────────────
    default_output_dir: Path = Path("./output")
    default_slide_count: int = 10
    default_theme: str = "dark"

    # ── Cache ───────────────────────────────────────────────────────────────
    cache_dir: Path = CACHE_DIR

    @property
    def image_cache_dir(self) -> Path:
        return self.cache_dir / "images"

    @property
    def icon_cache_dir(self) -> Path:
        return self.cache_dir / "icons"


settings = Settings()
