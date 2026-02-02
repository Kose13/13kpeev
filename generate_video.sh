#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-video.txt

python generate_video.py \
  --data plovdiv_weather_template.json \
  --output plovdiv_weather_2026-02-03.mp4
