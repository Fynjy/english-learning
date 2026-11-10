#!/usr/bin/env python3
"""
Validate index.html: check that cardsData is valid JSON with all required fields
and that card count matches the original lord_of_verbs.html.
"""
import re
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

def main():
    # Read built index.html
    content = (PROJECT_DIR / "index.html").read_text(encoding="utf-8")

    # Extract JSON array
    m = re.search(r"const cardsData = (\[.*?\]);", content, re.DOTALL)
    assert m, "Could not find cardsData JSON array in index.html"
    data = json.loads(m.group(1))
    print(f"\u2705 Parsed {len(data)} cards from index.html")

    # Check required fields
    required = ["chapter", "verb", "v2", "v3", "sit", "success", "fail"]
    for i, card in enumerate(data):
        missing = [k for k in required if k not in card]
        if missing:
            print(f"\u274c Card {i+1} ({card.get('verb', '?')}) missing: {missing}")
            return 1
    print("\u2705 All cards have all required fields")

    # Compare with original
    orig = (PROJECT_DIR / "lord_of_verbs.html").read_text(encoding="utf-8")
    orig_count = orig.count("chapter:")
    new_count = content.count('"chapter":')
    
    if orig_count == 35:
        print(f"\u2705 Original has 35 chapter references")
    else:
        print(f"\u26a0\ufe0f Original has {orig_count} chapter references (expected 35)")
    
    print(f"New index.html: {new_count} chapter references")

    if orig_count == 35 and new_count == 35:
        print("\u2705 Card count matches original!")
    else:
        print(f"\u274c Mismatch: original={orig_count}, new={new_count}")
        return 1

    print(f"\nSummary:")
    print(f"  Cards: {len(data)}")
    print(f"  Fields: all verified")
    print(f"  Source: {PROJECT_DIR / 'index.html'}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
