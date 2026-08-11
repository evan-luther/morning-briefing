#!/usr/bin/env python3
"""Build today's public Philadelphia briefing from live public data."""
from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[1]
TZ = ZoneInfo("America/New_York")
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=39.9526&longitude=-75.1652"
    "&current=temperature_2m,apparent_temperature,weather_code"
    "&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    "&temperature_unit=fahrenheit&timezone=America%2FNew_York&forecast_days=1"
)
NEWS_URL = "https://feeds.npr.org/1001/rss.xml"

WEATHER = {
    0: "Clear",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Foggy",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Steady drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Passing showers",
    81: "Rain showers",
    82: "Heavy showers",
    95: "Thunderstorms",
    96: "Thunderstorms",
    99: "Thunderstorms",
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "MorningBriefing/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def short_time(value: str) -> str:
    parsed = dt.datetime.fromisoformat(value).replace(tzinfo=TZ)
    return parsed.strftime("%-I:%M %p")


def load_weather() -> dict:
    payload = json.loads(fetch(WEATHER_URL))
    current = payload["current"]
    daily = payload["daily"]
    code = int(current["weather_code"])
    apparent = round(float(current["apparent_temperature"]))
    rain = int(daily["precipitation_probability_max"][0] or 0)
    condition = WEATHER.get(code, "Variable conditions")
    summary = f"{condition}. Feels like {apparent}°. Rain chance {rain}%."
    return {
        "current": round(float(current["temperature_2m"])),
        "high": round(float(daily["temperature_2m_max"][0])),
        "low": round(float(daily["temperature_2m_min"][0])),
        "rain": rain,
        "sunrise": short_time(daily["sunrise"][0]),
        "sunset": short_time(daily["sunset"][0]),
        "summary": summary,
    }


def load_stories() -> list[dict[str, str]]:
    root = ET.fromstring(fetch(NEWS_URL))
    stories = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip().replace("—", "-").replace("–", "-")
        link = (item.findtext("link") or "").strip()
        if title and link:
            stories.append({"title": title, "link": link, "source": "NPR"})
        if len(stories) == 3:
            break
    if len(stories) < 3:
        raise RuntimeError("NPR feed returned fewer than three stories")
    return stories


def story_markup(stories: list[dict[str, str]]) -> str:
    rows = []
    for index, story in enumerate(stories, 1):
        rows.append(
            f'<a class="story" href="{html.escape(story["link"], quote=True)}" '
            f'target="_blank" rel="noreferrer">'
            f'<span class="story-index">{index:02d}</span>'
            f'<span class="story-title">{html.escape(story["title"])}</span>'
            f'<span class="story-source">{html.escape(story["source"])}</span>'
            "</a>"
        )
    return "\n        ".join(rows)


def main() -> None:
    now = dt.datetime.now(TZ)
    weather = load_weather()
    stories = load_stories()
    replacements = {
        "{{DATE_ISO}}": now.date().isoformat(),
        "{{DATE_LONG}}": now.strftime("%A, %B %-d"),
        "{{CURRENT_TEMP}}": str(weather["current"]),
        "{{HIGH_TEMP}}": str(weather["high"]),
        "{{LOW_TEMP}}": str(weather["low"]),
        "{{RAIN_CHANCE}}": str(weather["rain"]),
        "{{SUNRISE}}": weather["sunrise"],
        "{{SUNSET}}": weather["sunset"],
        "{{WEATHER_SUMMARY}}": html.escape(weather["summary"], quote=True),
        "{{STORIES}}": story_markup(stories),
    }
    page = (ROOT / "template.html").read_text()
    for needle, value in replacements.items():
        page = page.replace(needle, value)
    if "{{" in page:
        raise RuntimeError("unresolved template marker")
    (ROOT / "index.html").write_text(page)
    (ROOT / "briefing.json").write_text(
        json.dumps({"generated_at": now.isoformat(), "weather": weather, "stories": stories}, indent=2) + "\n"
    )
    print(f"Built briefing for {now.date().isoformat()}: {weather['summary']}")


if __name__ == "__main__":
    main()
