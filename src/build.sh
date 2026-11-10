#!/bin/bash
# Build script for "Хранители Глаголов" game
# Calls build.py to combine src/template.html with questions/*.json into index.html

set -e
cd "$(dirname "$0")/.."
python3 src/build.py
