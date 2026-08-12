import json
from pathlib import Path
from datetime import datetime

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

WIDTH = 860
CELL = 13
GAP = 4
ROWS = 7
COLS = 53


def load_data():
    if not DATA.exists():
        return []

    with open(DATA, "r", encoding="utf-8") as f:
        obj = json.load(f)

    if isinstance(obj, dict):
        days = obj.get("days", [])
    else:
        days = obj

    return days


def get_count(day):
    if isinstance(day, dict):
        return int(day.get("count", day.get("contributions", 0)))
    return int(day)


def draw_heatmap(days):
    max_count = max([get_count(d) for d in days] or [1])

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="125" viewBox="0 0 {WIDTH} 125">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
    ]

    for i, day in enumerate(days[-COLS * ROWS:]):
        count = get_count(day)

        col = i // ROWS
        row = i % ROWS

        x = 10 + col * (CELL + GAP)
        y = 10 + row * (CELL + GAP)

        if count == 0:
            level = 0
        else:
            level = min(
                5,
                max(1, int((count / max_count) * 5))
            )

        color = PALETTE[level]

        svg.append(
            f'<rect x="{x}" y="{y}" '
            f'width="{CELL}" height="{CELL}" '
            f'rx="3" fill="{color}">'
            f'<title>{count} contributions</title>'
            f'</rect>'
        )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    days = load_data()
    svg = draw_heatmap(days)

    OUT.write_text(svg, encoding="utf-8")
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
