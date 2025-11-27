# embeddings.py

from typing import Optional
import numpy as np
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

from scraping import fetch_html

# Load once, reuse
_model = SentenceTransformer("all-MiniLM-L6-v2")

# Simple in-memory cache so we don't recompute embeddings for the same title
_embedding_cache: dict[str, np.ndarray] = {}


def _extract_intro_text(html: str) -> str:
    """
    Extract the first 1–2 non-empty paragraphs from the article body.
    Fallback to empty string if nothing useful.
    """
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"id": "mw-content-text"})
    if content is None:
        return ""

    paragraphs = content.find_all("p", recursive=True)
    texts: list[str] = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:
            texts.append(text)
        if len(texts) >= 2:
            break

    return " ".join(texts)


def _embed_text(text: str) -> np.ndarray:
    """Encode text into a vector."""
    return _model.encode([text])[0]


def get_page_embedding(title: str) -> np.ndarray:
    """
    Get (and cache) an embedding for a Wikipedia page.

    Strategy:
      - Fetch HTML
      - Extract intro paragraphs
      - If intro is empty, fall back to the title itself
    """
    if title in _embedding_cache:
        return _embedding_cache[title]

    html = fetch_html(title)
    intro = _extract_intro_text(html)
    text = intro if intro else title.replace("_", " ")

    vec = _embed_text(text)
    _embedding_cache[title] = vec
    return vec

from typing import List, Dict
import numpy as np

# existing:
# _model = SentenceTransformer("all-MiniLM-L6-v2")
# _embedding_cache: dict[str, np.ndarray] = {}
# _extract_intro_text(...)
# _embed_text(...)
# get_page_embedding(...)

def get_page_embeddings_batch(titles: List[str]) -> Dict[str, np.ndarray]:
    """
    Get embeddings for a list of page titles, using batching for speed.

    - Uses cache when available
    - Only fetches + encodes for uncached titles
    - Returns a dict: title -> embedding
    """
    result: Dict[str, np.ndarray] = {}

    # 1) Fill from cache
    uncached: List[str] = []
    for title in titles:
        if title in _embedding_cache:
            result[title] = _embedding_cache[title]
        else:
            uncached.append(title)

    if not uncached:
        return result

    # 2) Fetch HTML + intro texts for uncached titles
    texts: List[str] = []
    for title in uncached:
        html = fetch_html(title)
        intro = _extract_intro_text(html)
        text = intro if intro else title.replace("_", " ")
        texts.append(text)

    # 3) Batch-encode all texts in one go
    #    (you can tweak batch_size if you want)
    embeddings = _model.encode(texts, batch_size=32)

    # 4) Store in cache and result
    for title, vec in zip(uncached, embeddings):
        vec = np.asarray(vec)
        _embedding_cache[title] = vec
        result[title] = vec

    return result