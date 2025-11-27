#!/usr/bin/env python

import sys
from typing import List, Tuple

import numpy as np

from scraping import fetch_html, extract_wiki_links
from embeddings import get_page_embedding, get_page_embeddings_batch

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a, b) / denom)


def choose_next_link(
    current_title: str,
    target_emb: np.ndarray,
    max_links: int = 100,
    visited: set[str] | None = None,
) -> str | None:
    """
    From the current page, pick the outbound link whose embedding
    is closest (by cosine similarity) to the target embedding.

    Uses batched embedding for candidate links to speed things up.
    """
    # Fetch links from current page
    html = fetch_html(current_title)
    links = extract_wiki_links(html)

    if not links:
        return None

    # Filter out visited nodes if provided
    if visited is not None:
        links = [t for t in links if t not in visited]

    if not links:
        return None

    # Limit number of links to consider (optional, for speed)
    if max_links is not None and len(links) > max_links:
        links = links[:max_links]

    # Batch-get embeddings for all candidate links
    emb_dict = get_page_embeddings_batch(links)

    best_title = None
    best_score = -1.0

    for title, emb in emb_dict.items():
        score = cosine_sim(emb, target_emb)
        if score > best_score:
            best_score = score
            best_title = title

    return best_title

def speedrun(start_title: str, target_title: str, max_steps: int = 20) -> tuple[list[str], bool]:
    """
    Greedy semantic speedrun:
      - start at start_title
      - at each step, pick the link whose embedding is closest to target
      - stop if we hit target, max_steps, or get stuck

    Returns:
      (path, reached_target)
    """
    current = start_title
    path: list[str] = [current]
    visited: set[str] = set()

    # Compute target embedding once
    target_emb = get_page_embedding(target_title)

    for step in range(max_steps):
        print("Current - ", current)

        if current == target_title:
            return path, True

        visited.add(current)

        next_title = choose_next_link(
            current_title=current,
            target_emb=target_emb,
            max_links=50,          # you can tune this
            visited=visited,
        )
        if next_title is None:
            break

        if next_title in visited:
            break

        path.append(next_title)
        current = next_title

    return path, current == target_title


def main():
    if len(sys.argv) < 3:
        start_title = "potato"
        target_title = "France"
    else:
        start_title = sys.argv[1]
        target_title = sys.argv[2]

    print(f"Starting speedrun: {start_title} → {target_title}")
    path, reached = speedrun(start_title, target_title, max_steps=15)

    print("\nPath:")
    for i, p in enumerate(path):
        print(f"{i:2d}: {p}")

    print("\nReached target:", reached)


if __name__ == "__main__":
    main()