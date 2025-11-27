#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import time
import threading
import numpy as np

from embeddings import get_page_embedding
from speedrun import choose_next_link


START_TITLE = "One Piece"      # you can change these
TARGET_TITLE = "Cheeseburger"
MAX_STEPS = 15
MAX_LINKS = 50


class SpeedrunGUI:
    def __init__(self, root):
        self.root = root
        root.title("Wikipedia Speedrun")

        # ---------------- UI Layout ----------------
        tk.Label(root, text="Source Page:").grid(row=0, column=0, sticky="w")
        self.src_entry = tk.Entry(root, width=40)
        self.src_entry.insert(0, START_TITLE)
        self.src_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Target Page:").grid(row=1, column=0, sticky="w")
        self.tgt_entry = tk.Entry(root, width=40)
        self.tgt_entry.insert(0, TARGET_TITLE)
        self.tgt_entry.grid(row=1, column=1, padx=5, pady=5)

        self.start_button = tk.Button(
            root,
            text="Start Speedrun",
            command=self.start_speedrun_thread
        )
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        sep = ttk.Separator(root, orient="horizontal")
        sep.grid(row=3, columnspan=2, sticky="ew", pady=10)

        # Live display fields
        self.status_vars = {
            "current": tk.StringVar(),
            "step": tk.StringVar(),
            "links": tk.StringVar(),
            "elapsed": tk.StringVar(),
        }

        tk.Label(root, text="Current Page:").grid(row=4, column=0, sticky="w")
        tk.Label(root, textvariable=self.status_vars["current"]).grid(row=4, column=1, sticky="w")

        tk.Label(root, text="Step:").grid(row=5, column=0, sticky="w")
        tk.Label(root, textvariable=self.status_vars["step"]).grid(row=5, column=1, sticky="w")

        tk.Label(root, text="Links Clicked:").grid(row=6, column=0, sticky="w")
        tk.Label(root, textvariable=self.status_vars["links"]).grid(row=6, column=1, sticky="w")

        tk.Label(root, text="Elapsed Time:").grid(row=7, column=0, sticky="w")
        tk.Label(root, textvariable=self.status_vars["elapsed"]).grid(row=7, column=1, sticky="w")

        tk.Label(root, text="Path Taken:").grid(row=8, column=0, sticky="nw")
        self.path_text = tk.Text(root, width=50, height=10)
        self.path_text.grid(row=8, column=1, padx=5, pady=10)

        # Timer state
        self.timer_running = False
        self.start_time = None

        # Hover/click styling disabled

    # ---------------- Thread Wrapper ----------------
    def start_speedrun_thread(self):
        # Prevent starting another run while one is active
        if self.timer_running:
            return

        self.start_time = time.perf_counter()
        self.timer_running = True
        self.update_timer()

        thread = threading.Thread(target=self.speedrun, daemon=True)
        thread.start()

    def update_timer(self):
        if not self.timer_running or self.start_time is None:
            return

        elapsed = time.perf_counter() - self.start_time
        self.status_vars["elapsed"].set(f"{elapsed:.2f} s")
        # Schedule next update
        self.root.after(100, self.update_timer)

    def _on_start_hover(self, event):
        pass

    def _on_start_leave(self, event):
        pass

    def _on_start_press(self, event):
        pass

    def _on_start_release(self, event):
        pass

    # ---------------- Core Logic ----------------
    def speedrun(self):
        src = self.src_entry.get().strip()
        tgt = self.tgt_entry.get().strip()

        current = src
        visited = set()
        path = [current]

        # Reset path display and show initial page
        self.path_text.delete("1.0", tk.END)
        self.path_text.insert(tk.END, current)

        target_emb: np.ndarray = get_page_embedding(tgt)

        start_time = time.perf_counter()

        for step in range(MAX_STEPS):
            # Update UI for current state
            self.status_vars["current"].set(current)
            self.status_vars["step"].set(str(step))
            self.status_vars["links"].set(str(len(path) - 1))

            self.root.update_idletasks()  # refresh UI

            # Check if target reached
            if current == tgt:
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

            # Live update of the path as a chain
            self.path_text.delete("1.0", tk.END)
            self.path_text.insert(tk.END, " -> ".join(path))

        # Stop the live timer
        self.timer_running = False

        # Final state for current page
        self.status_vars["current"].set(f"{current} (finished)")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedrunGUI(root)
    root.mainloop()