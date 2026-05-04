"""
genppt CLI — Typer-based command-line interface.

Usage:
    genppt generate --topic "AI in healthcare" --slides 10 --theme dark
    genppt generate --topic "..." --output my_deck.pptx
    genppt list themes
    genppt list icons
    genppt cache clear
    genppt cache status
"""

import shutil
from pathlib import Path

import typer
from rich import print as rprint
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from genppt.config import settings

app = typer.Typer(
    name="genppt",
    help="AI-powered PowerPoint generator using LangGraph + open-source resources",
    rich_markup_mode="rich",
)
console = Console()

# ── generate ─────────────────────────────────────────────────────────────────

@app.command()
def generate(
    topic: str = typer.Option(..., "--topic", "-t", help="Presentation topic or prompt"),
    slides: int = typer.Option(
        settings.default_slide_count, "--slides", "-n", help="Number of slides"
    ),
    theme: str = typer.Option(
        settings.default_theme, "--theme", help="Theme: dark | corporate | minimalist"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="Output .pptx file path"
    ),
    template: str = typer.Option(
        None, "--template", help="Custom .pptx template file"
    ),
):
    """Generate a presentation from a topic prompt."""
    if output is None:
        out_dir = settings.default_output_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        output = str(out_dir / "presentation.pptx")

    rprint(f"\n[bold cyan]🎯 Topic:[/bold cyan] {topic}")
    rprint(f"[bold cyan]📊 Slides:[/bold cyan] {slides}")
    rprint(f"[bold cyan]🎨 Theme:[/bold cyan] {theme}")
    rprint(f"[bold cyan]📄 Output:[/bold cyan] {output}\n")

    from genppt.agent.graph import graph

    initial_state = {
        "topic": topic,
        "slide_count": slides,
        "theme": theme,
        "template_path": template,
        "output_path": output,
        "context": None,
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Running AI pipeline…", total=None)

        try:
            result = graph.invoke(initial_state)
        except Exception as e:
            progress.stop()
            rprint(f"\n[bold red]❌ Error:[/bold red] {e}")
            raise typer.Exit(code=1)

        progress.update(task, description="[green]✅ Done!")

    pptx_path = result.get("pptx_path", output)
    rprint(f"\n[bold green]✅ Presentation saved to:[/bold green] {pptx_path}")
    outline = result.get("outline")
    if outline:
        rprint(f"[dim]   Title: {outline.presentation_title}[/dim]")
        rprint(f"[dim]   Slides: {len(outline.slides)}[/dim]")


# ── list ─────────────────────────────────────────────────────────────────────

list_app = typer.Typer(help="List available resources")
app.add_typer(list_app, name="list")


@list_app.command("themes")
def list_themes():
    """Show available presentation themes."""
    from genppt.renderer.themes import THEMES

    table = Table(title="Available Themes")
    table.add_column("Name", style="cyan bold")
    table.add_column("Background", style="dim")
    table.add_column("Accent", style="dim")

    for name, t in THEMES.items():
        table.add_row(
            name,
            f"rgb{t.slide_bg}",
            f"rgb{t.accent_color}",
        )
    console.print(table)


@list_app.command("icons")
def list_icons():
    """Show available icon sets and their cache status."""
    icon_dir = settings.icon_cache_dir
    table = Table(title="Icon Sets")
    table.add_column("Set", style="cyan bold")
    table.add_column("Cached", style="dim")
    table.add_column("Count", style="dim")

    sets = ["tabler", "bootstrap", "heroicons", "feather", "simple-icons"]
    for s in sets:
        d = icon_dir / s
        if d.exists():
            count = len(list(d.glob("*.svg")))
            table.add_row(s, "✅", str(count))
        else:
            table.add_row(s, "❌ (will download on first use)", "—")
    console.print(table)


# ── cache ────────────────────────────────────────────────────────────────────

cache_app = typer.Typer(help="Manage local asset cache")
app.add_typer(cache_app, name="cache")


@cache_app.command("status")
def cache_status():
    """Show cache directory sizes."""
    for label, d in [("images", settings.image_cache_dir), ("icons", settings.icon_cache_dir)]:
        if d.exists():
            total = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
            mb = total / (1024 * 1024)
            rprint(f"  [cyan]{label}[/cyan]: {d}  ({mb:.1f} MB)")
        else:
            rprint(f"  [cyan]{label}[/cyan]: not created yet")


@cache_app.command("clear")
def cache_clear():
    """Delete all cached images and icons."""
    for d in [settings.image_cache_dir, settings.icon_cache_dir]:
        if d.exists():
            shutil.rmtree(d)
            rprint(f"  [yellow]Cleared:[/yellow] {d}")
    rprint("[green]Cache cleared.[/green]")


if __name__ == "__main__":
    app()
