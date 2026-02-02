#!/usr/bin/env python3
"""Generate a 4K H.264 MP4 weather storyboard video for Plovdiv (2026-02-03).

This script creates a simple, hour-by-hour visual plan with on-screen text.
It uses Pillow for rendering and imageio's ffmpeg backend for encoding.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Iterable, Mapping

from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np

WIDTH = 3840
HEIGHT = 2160
FPS = 30
SEGMENT_SECONDS = 5
BACKGROUND = (10, 16, 26)
ACCENT = (255, 255, 255)

DEFAULT_WEATHER = {
    "temp_c": "__",
    "wind_kmh": "__",
    "precip_mm": "__",
    "cloud_pct": "__",
}


def find_font() -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, 90)
    return ImageFont.load_default()


def draw_frame(hour: int, date: dt.date, weather: Mapping[str, str]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    title_font = find_font()
    body_font = ImageFont.truetype(title_font.path, 72) if hasattr(title_font, "path") else title_font

    title = f"Пловдив • {date.strftime('%d.%m.%Y')}"
    subtitle = "Почасова прогноза • DJI Osmo Action 5 Pro стил"
    timestamp = f"{hour:02d}:00"
    metrics = (
        f"T: {weather['temp_c']}°C   Вятър: {weather['wind_kmh']} km/h   "
        f"Валежи: {weather['precip_mm']} mm   Облачност: {weather['cloud_pct']}%"
    )

    draw.text((140, 140), title, fill=ACCENT, font=title_font)
    draw.text((140, 260), subtitle, fill=(200, 210, 220), font=body_font)
    draw.text((140, 960), timestamp, fill=ACCENT, font=title_font)
    draw.text((140, 1150), metrics, fill=(220, 230, 240), font=body_font)

    return image


def iter_frames(
    hours: Iterable[int],
    date: dt.date,
    segment_seconds: int,
    hourly_weather: Mapping[int, Mapping[str, str]] | None = None,
) -> Iterable[np.ndarray]:
    frames_per_segment = segment_seconds * FPS
    for hour in hours:
        weather = hourly_weather.get(hour, DEFAULT_WEATHER) if hourly_weather else DEFAULT_WEATHER
        frame_image = draw_frame(hour, date, weather)
        frame_array = np.array(frame_image)
        for _ in range(frames_per_segment):
            yield frame_array


def build_video(
    output: Path,
    date: dt.date,
    segment_seconds: int,
    hourly_weather: Mapping[int, Mapping[str, str]] | None = None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    frames = iter_frames(range(24), date, segment_seconds, hourly_weather)
    with imageio.get_writer(
        output,
        fps=FPS,
        codec="libx264",
        format="ffmpeg",
        bitrate="25M",
        macro_block_size=None,
    ) as writer:
        for frame in frames:
            writer.append_data(frame)


def load_weather(path: Path | None) -> tuple[dt.date, dict[int, dict[str, str]]]:
    if path is None:
        return dt.date(2026, 2, 3), {}
    data = json.loads(path.read_text(encoding="utf-8"))
    date = dt.datetime.strptime(data.get("date", "2026-02-03"), "%Y-%m-%d").date()
    hourly_weather: dict[int, dict[str, str]] = {}
    for entry in data.get("hours", []):
        hour = int(entry["hour"])
        hourly_weather[hour] = {
            "temp_c": str(entry.get("temp_c", "__")),
            "wind_kmh": str(entry.get("wind_kmh", "__")),
            "precip_mm": str(entry.get("precip_mm", "__")),
            "cloud_pct": str(entry.get("cloud_pct", "__")),
        }
    return date, hourly_weather


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("plovdiv_weather_2026-02-03.mp4"),
        help="Output MP4 path",
    )
    parser.add_argument(
        "--date",
        type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(),
        default=dt.date(2026, 2, 3),
        help="Date for the overlay (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="Optional JSON file with hourly weather data",
    )
    parser.add_argument(
        "--segment-seconds",
        type=int,
        default=SEGMENT_SECONDS,
        help="Seconds per hour segment (default: 5)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.data:
        date, hourly_weather = load_weather(args.data)
    else:
        date, hourly_weather = args.date, {}
    build_video(args.output, date, args.segment_seconds, hourly_weather)
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
