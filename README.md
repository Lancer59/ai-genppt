# ai-genppt

An AI-powered PowerPoint generation tool built with Python. `ai-genppt` accepts a presentation topic, outline, or prompt and produces a polished, content-rich `.pptx` file. 

The tool uses a **LangGraph agent** for multi-step orchestration and strictly leverages **100% open-source or free resources** for images and icons (with Azure OpenAI or any OpenAI-compatible API providing the LLM capabilities).

---

## 🌟 Features

- **Agentic Generation Pipeline:** Powered by LangGraph (`plan_slides` → `fetch_images` ∥ `fetch_icons` → `build_pptx`).
- **Open-Source Image Fetching:** Automatically searches and integrates high-quality photography from **Wikimedia Commons** and **Openverse** (with **Lorem Picsum** fallbacks).
- **Offline Icon Caching:** Automatically downloads and indexes thousands of SVG icons from **Tabler**, **Bootstrap**, **Heroicons**, **Feather**, and **Simple Icons**. SVGs are converted to PNGs on the fly.
- **7 Slide Layouts:** Supports specialized layouts including Title, Section Header, Content (bullets + image), Two-Column Comparison, Full-Bleed Image, Stats Callout, and Closing/Thank You.
- **3 Built-in Themes:** Choose from `dark`, `corporate`, or `minimalist`.
- **Custom Templates:** You can supply your own branded `.pptx` file for the tool to populate.

---

## 📦 Installation

This project requires **Python 3.11+**.

```bash
# 1. Clone the repository and cd into it
git clone https://github.com/lancer59/ai-genppt.git
cd ai-genppt

# 2. Create and activate a virtual environment
python -m venv .venv
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# 3. Install the package
pip install -e .
```

---

## ⚙️ Configuration

Copy the `.env.example` file to create a `.env` file in the project root:

```bash
cp .env.example .env
```

You must configure **at least one** LLM provider. By default, `ai-genppt` looks for Azure OpenAI credentials. If you want to use a generic OpenAI-compatible API (like standard OpenAI, Ollama, Groq, etc.), comment out the Azure variables and set `OPENAI_API_KEY` (and `OPENAI_BASE_URL` if needed).

```env
# ── LLM: Azure OpenAI (primary) ───────────────────────────────────────────────
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_OUTPUT_DIR=./output
DEFAULT_SLIDE_COUNT=10
DEFAULT_THEME=dark
```

---

## 🚀 Usage

`ai-genppt` comes with a rich CLI interface.

### Generate a Presentation

```bash
# Generate a 10-slide deck on AI in healthcare using the corporate theme
genppt generate --topic "AI in healthcare" --slides 10 --theme corporate --output ./my-deck.pptx

# Let the tool decide the best slide count
genppt generate --topic "A pitch deck for a new sustainable shoe brand"

# Use a custom branded PPTX template
genppt generate --topic "Quarterly Earnings Report" --template ./my_brand_template.pptx
```

### Inspect Available Resources

```bash
# View available themes
genppt list themes

# View available icon sets and their local cache status
genppt list icons
```

### Manage Local Cache

Images and icons are aggressively cached locally in `~/.ai-genppt/cache` to speed up future generations and allow offline usage of previously downloaded icons.

```bash
# See how much space the cache is using
genppt cache status

# Clear the cache
genppt cache clear
```

---

## 🏗️ Architecture (LangGraph)

The core pipeline is orchestrated using a `LangGraph` StateGraph located in `genppt/agent/`.

1. **`plan_slides`**: The LLM creates a structured `SlideOutline` dictating layouts, bullets, photo search queries, and icon names.
2. **`fetch_assets`**: Uses `asyncio.gather` to perform a parallel fan-out search:
   - Queries Wikimedia and Openverse for requested photos.
   - Searches local icon sets (downloading them from GitHub releases if it's the first run) and converts SVG to PNG.
3. **`build_pptx`**: Feeds the outline and the fetched local file paths to `python-pptx`, applying the selected theme and assembling the slides.

---

## 🛠️ Development

If you want to contribute or run the test suite:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```
