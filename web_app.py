# web_app.py
import time
import streamlit as st

from embeddings import get_page_embedding
from speedrun import choose_next_link

MAX_STEPS = 15
MAX_LINKS = 50

st.title("Wikipedia SpeedRun AI")

source = st.text_input("Source article", "One Piece")
target = st.text_input("Target article", "Burger King")

if st.button("Start speedrun"):
    if not source or not target:
        st.warning("Please enter both source and target.")
    else:
        with st.spinner("Running speedrun... (downloading model the first time may take a bit)"):
            current = source
            visited = set()
            path = [current]

            target_emb = get_page_embedding(target)

            start_time = time.perf_counter()

            for step in range(MAX_STEPS):
                if current == target:
                    break

                visited.add(current)
                next_title = choose_next_link(
                    current,
                    target_emb,
                    MAX_LINKS,
                    visited,
                )

                if next_title is None or next_title in visited:
                    break

                path.append(next_title)
                current = next_title

            elapsed = time.perf_counter() - start_time

        st.subheader("Result")
        st.write(f"Reached target: **{current == target}**")
        st.write(f"Steps taken: **{len(path) - 1}**")
        st.write(f"Time: **{elapsed:.2f} s**")

        st.subheader("Path")
        st.write(" → ".join(path))