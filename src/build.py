#!/usr/bin/env python3
"""
Build script for "Хранители Глаголов" game.
Combines src/template.html with questions/*.json into index.html.
"""

import json
import glob
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
TEMPLATE = SCRIPT_DIR / "template.html"
QUESTIONS_DIR = PROJECT_DIR / "questions"
OUTPUT = PROJECT_DIR / "lord_of_verbs.html"

def main():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()

    cards = []
    json_files = sorted(QUESTIONS_DIR.glob("*.json"))
    for fpath in json_files:
        with open(fpath, "r", encoding="utf-8") as f:
            cards.append(json.load(f))

    cards_json = json.dumps(cards, ensure_ascii=False, indent=2)
    output = template.replace("CARDS_DATA", cards_json)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(output)

    first = json_files[0].name
    last = json_files[-1].name
    print(f"Built {OUTPUT.name} with {len(cards)} cards ({first} — {last})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
