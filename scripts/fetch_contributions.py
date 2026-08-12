import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

USERNAME = "iceman0009"

URL = f"https://github.com/users/iceman0009/contributions"

OUT = Path("data/contributions.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    count_text = cell.get("data-level", "0")

    try:
        level = int(count_text)
    except ValueError:
        level = 0

    days.append({
        "date": date,
        "level": level,
        "count": level
    })

data = {
    "username": iceman0009,
    "days": days
}

OUT.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print(f"Saved {len(days)} contribution days to {OUT}")
