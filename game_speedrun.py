#!/usr/bin/env python

import time
from typing import Set, List

import numpy as np

from embeddings import get_page_embedding
from speedrun import choose_next_link


START_TITLE = "One Piece"
TARGET_TITLE = "Cheeseburger"
MAX_STEPS = 15
MAX_LINKS_PER_STEP = 50


def run_game(
    start_title: str = START_TITLE,
    target_title: str = TARGET_TITLE,
    max_steps: int = MAX_STEPS,
    max_links: int = MAX_LINKS_PER_STEP,
) -> None:
    """
    Game interface for the Wikipedia speedrun agent.

    - Prints current page, steps taken, and elapsed time as it runs
    """
    current = start_title
    visited: Set[str] = set()
    path: List[str] = [current]

    print(f"=== Wikipedia Speedrun Game ===")
    print(f"Source : {start_title}")
    print(f"Target : {target_title}")
    print(f"Max steps: {max_steps}\n")

    # Compute target embedding once
    target_emb: np.ndarray = get_page_embedding(target_title)

    start_time = time.perf_counter()

    for step in range(max_steps):
        elapsed = time.perf_counter() - start_time
        links_clicked = len(path) - 1

        # Live status
        print(
            f"Step {step:2d} | "
            f"Current: {current} | "
            f"Links clicked: {links_clicked} | "
            f"Elapsed: {elapsed:5.2f}s"
        )

        # Check if we already arrived
        if current == target_title:
            print("\n🎯 Target reached!")
            break

        visited.add(current)

        # Ask the agent for the next move
        next_title = choose_next_link(
            current_title=current,
            target_emb=target_emb,
            max_links=max_links,
            visited=visited,
        )

        if next_title is None:
            print("\n⚠️ No valid next link found. Stopping.")
            break

        if next_title in visited:
            print(f"\n🔁 Next link {next_title} was already visited. Stopping to avoid loop.")
            break

        # "Click" the link
        path.append(next_title)
        current = next_title

    end_time = time.perf_counter()
    total_elapsed = end_time - start_time
    total_clicks = len(path) - 1

    print("\n=== Game Over ===")
    print(f"Reached target : {current == target_title}")
    print(f"Final page     : {current}")
    print(f"Links clicked  : {total_clicks}")
    print(f"Total time     : {total_elapsed:5.2f}s\n")

    print("Path followed:")
    for i, title in enumerate(path):
        print(f"{i:2d}: {title}")


if __name__ == "__main__":
    run_game()