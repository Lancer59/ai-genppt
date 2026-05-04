import hashlib


def get_picsum_url(query: str = "", width: int = 1920, height: int = 1080) -> str:
    """
    Generate a deterministic Lorem Picsum URL seeded from the query string.
    Always returns a valid image — used as a final fallback.
    """
    seed = int(hashlib.md5(query.encode()).hexdigest(), 16) % 1000 if query else 42
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"
