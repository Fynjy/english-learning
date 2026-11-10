#!/usr/bin/env python3
"""
Script to add <b> tags around Russian verbs in each card's sit field.
Maps each English verb to its Russian counterpart in the sit text.
"""

import json
import glob
import re
import os

# Mapping of English verb -> Russian word to bold in sit
# (and optional rephrase if the word needs to be changed)
VERB_MAP = {
    "FIND":   { "word": "находите" },
    "GO":     { "word": "идти" },
    "RUN":    { "word": "бежать" },
    "HIDE":   { "word": "спрятаться" },
    "MEET":   { "word": "встретили" },
    "SEE":    { "word": "смотрите" },
    "BRING":  { "word": "понесет" },
    "KNOW":   { "word": "знает" },
    "HEAR":   { "word": "услышать" },
    "FIGHT":  { "word": "сражаетесь" },
    "BREAK":  { "word": "разрушает" },
    "FALL":   { "word": "падая" },
    "COME":   { "word": "приходите", "rephrase": True,
                "old_word": "идете" },
    "GIVE":   { "word": "дает" },
    "BECOME": { "word": "становиться" },
    "TAKE":   { "word": "берет" },
    "CATCH":  { "word": "хватают" },
    "EAT":    { "word": "есть" },
    "DRINK":  { "word": "пить" },
    "SPEAK":  { "word": "говорить" },
    "RIDE":   { "word": "скакать" },
    "SING":   { "word": "запоют" },
    "BUILD":  { "word": "строит" },
    "SAY":    { "word": "сказать" },
    "CHOOSE": { "word": "выбрать" },
    "FORGET": { "word": "забыть" },
    "WRITE":  { "word": "написать" },
    "THINK":  { "word": "придумать" },
    "READ":   { "word": "прочитать" },
    "LOSE":   { "word": "теряют" },
    "MAKE":   { "word": "сделать" },
    "FLY":    { "word": "летать" },
    "WIN":    { "word": "победили" },
    "DO":     { "word": "сделали" },
    "SLEEP":  { "word": "поспать" },
}

QUESTIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "questions")


def bold_word_in_sit(sit, word, verb, rephrase_info=None):
    """Bold the given word in the sit text (case-insensitive matching)."""
    if rephrase_info:
        # Replace old word with new word first (case-insensitive)
        old = rephrase_info["old_word"]
        # Use case-insensitive replacement for the rephrase
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        sit = pattern.sub(word, sit, count=1)

    # Highlight the word (case-insensitive, first occurrence)
    # Build a regex that matches the word case-insensitively
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    match = pattern.search(sit)
    if match:
        start, end = match.start(), match.end()
        original = sit[start:end]
        sit = sit[:start] + f'<span class="hl">{original}</span>' + sit[end:]
        return sit
    else:
        print(f"  WARNING: word '{word}' not found in sit for verb '{verb}'!")
        print(f"    sit: {sit[:100]}...")
        return sit


def main():
    files = sorted(glob.glob(os.path.join(QUESTIONS_DIR, "*.json")))
    print(f"Found {len(files)} question files.")

    for fpath in files:
        basename = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        verb = data["verb"]
        sit = data["sit"]

        # Strip any existing highlight tags to allow re-running safely
        sit = sit.replace("<b>", "").replace("</b>", "")
        sit = sit.replace('<span class="hl">', "").replace("</span>", "")

        if verb not in VERB_MAP:
            print(f"  SKIP {basename}: verb '{verb}' not in map")
            continue

        info = VERB_MAP[verb]
        word = info["word"]
        rephrase_info = info if info.get("rephrase") else None

        new_sit = bold_word_in_sit(sit, word, verb, rephrase_info)

        if new_sit != sit:
            data["sit"] = new_sit
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  OK   {basename}: highlighted '{word}'")
        else:
            print(f"  SAME {basename}: no change needed")

    print("\nDone!")


if __name__ == "__main__":
    main()