📘 Wikipedia SpeedRun AI

AI-powered semantic navigation through Wikipedia using embeddings, batching, and a Tkinter live GUI

<p align="center">
  <img src="assets/gui_demo.png" width="550">
</p>



⸻

🏷️ Badges

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" />
  <img src="https://img.shields.io/github/stars/deepanshudaw/SpeedRun?style=social" />
  <img src="https://img.shields.io/github/repo-size/deepanshudaw/SpeedRun" />
  <img src="https://img.shields.io/github/last-commit/deepanshudaw/SpeedRun" />
  <img src="https://img.shields.io/github/issues/deepanshudaw/SpeedRun" />
  <img src="https://img.shields.io/github/issues-pr/deepanshudaw/SpeedRun" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
</p>



⸻

🧠 Overview

This project implements a Wikipedia Speedrun Agent — an AI that tries to navigate from one Wikipedia page to another using semantic embeddings, not brute-force hyperlink chasing.

It uses:
	•	MiniLM-L6-v2 sentence-transformer embeddings
	•	Batch encoding for dramatic speedup
	•	Scraping + link graph extraction
	•	A full Tkinter GUI with:
	•	live timer
	•	live path updates (A → B → C → ...)
	•	animated Start button
	•	blue-themed interface

Perfect as a showcase project in your AI portfolio.

⸻

🌟 GUI Images

🖼️ Main Interface


<p align="center">
  <img src="assets/gui_blue_theme.png" width="600">
</p>



⸻

🖼️ Live Speedrun

<p align="center">
  <img src="assets/gui_running.png" width="600">
</p>



⸻

🖼️ Path Visualization

<p align="center">
  <img src="assets/path_demo.png" width="600">
</p>



⸻

🚀 Features

✔️ AI-driven semantic navigation

Each hop is chosen via cosine similarity:

next = argmax ( cosine(embedding(link), embedding(target)) )

✔️ Real-time GUI
	•	live timer
	•	current page status
	•	dynamic path chain
	•	animated button interactions
	•	blue theme

✔️ Highly optimized
	•	Batch embedding (1 model call instead of 100 per step)
	•	HTML caching
	•	Embedding caching
	•	Target embedding computed once

⸻

📂 Project Structure

SpeedRun/
│
├── scraping.py          # Wikipedia scraping
├── embeddings.py        # Batched transformer embeddings + caching
├── speedrun.py          # Core navigation logic
├── game_speedrun.py     # Terminal "live" version
├── tk_speedrun.py       # Tkinter GUI with timer + animations
├── assets/              # <-- put your screenshots here
│    ├── gui_demo.png
│    ├── gui_running.png
│    └── path_demo.png
│
└── README.md


⸻

🔧 Installation

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


⸻

▶️ Running the GUI

python tk_speedrun.py


⸻

▶️ Running Terminal Version

python game_speedrun.py


⸻

🧠 Technical Walkthrough

Embeddings
	•	Extracts intro paragraphs using BeautifulSoup
	•	Encodes them using MiniLM-L6-v2
	•	384-dimensional vectors

Batching

All candidate links are embedded at once:

model.encode(list_of_texts, batch_size=32)

This is the single largest performance gain.

Navigation
	•	Greedy semantic search
	•	Avoids revisiting pages
	•	Stops on loops, dead ends, or max steps

⸻

📈 Future Enhancements
	•	Beam search for multi-path exploration
	•	Streamlit web interface
	•	Real-time graph visualization
	•	Audio effects (link click, success, failure)
	•	Speed leaderboard
	•	GPT-powered reasoning mode

⸻

🧑‍💻 Author

Deepanshu Dawande
AI/ML Engineer • LLM Systems Developer
