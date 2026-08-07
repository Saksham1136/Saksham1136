import json
import re
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "Saksham1136"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def fetch_calendar():

    print(f"Fetching contributions for {USERNAME}...")
    print(URL)

    response = requests.get(
        URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    return response.text


def parse_calendar(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    days = []

    cells = soup.select(
        "td.ContributionCalendar-day[data-date][data-level]"
    )

    print(
        f"Found {len(cells)} contribution cells."
    )

    for cell in cells:

        date = cell.get("data-date")
        level = cell.get("data-level")

        if not date:
            continue

        try:
            level = int(level)
        except (TypeError, ValueError):
            level = 0

        # ----------------------------------------------------
        # GitHub now stores the contribution count in the
        # <tool-tip> immediately following the <td>.
        # ----------------------------------------------------

        count = 0

        tooltip = cell.find_next_sibling(
            "tool-tip"
        )

        if tooltip:

            text = tooltip.get_text(
                " ",
                strip=True
            )

            match = re.search(
                r"([\d,]+)\s+contributions?",
                text,
                re.IGNORECASE
            )

            if match:

                count = int(
                    match.group(1)
                    .replace(",", "")
                )

        days.append({
            "date": date,
            "count": count,
            "level": level,
        })

    return days


def calculate_stats(days):

    ordered = sorted(
        days,
        key=lambda day: day["date"]
    )

    total = sum(
        day["count"]
        for day in ordered
    )

    best_day = max(
        ordered,
        key=lambda day: day["count"],
        default=None
    )

    contribution_dates = {
        day["date"]
        for day in ordered
        if day["count"] > 0
    }

    # ========================================================
    # CURRENT STREAK
    # ========================================================

    current_streak = 0

    today = datetime.utcnow().date()

    check = today

    # GitHub data may end yesterday depending on UTC timing.
    # If today has no contribution, check yesterday.

    if check.isoformat() not in contribution_dates:

        check -= timedelta(days=1)

    while check.isoformat() in contribution_dates:

        current_streak += 1

        check -= timedelta(days=1)

    # ========================================================
    # LONGEST STREAK
    # ========================================================

    longest_streak = 0
    streak = 0
    previous = None

    for day in ordered:

        if day["count"] <= 0:

            streak = 0
            previous = None

            continue

        current = datetime.strptime(
            day["date"],
            "%Y-%m-%d"
        ).date()

        if (
            previous is not None
            and (current - previous).days == 1
        ):

            streak += 1

        else:

            streak = 1

        longest_streak = max(
            longest_streak,
            streak
        )

        previous = current

    return {
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
    }


def main():

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    html = fetch_calendar()

    days = parse_calendar(html)

    if not days:

        raise RuntimeError(
            "No contribution cells found."
        )

    stats = calculate_stats(days)

    data = {
        "username": USERNAME,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "days": days,
        "stats": stats,
    }

    OUTPUT.write_text(
        json.dumps(
            data,
            indent=2
        ),
        encoding="utf-8"
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print()
    print("================================")
    print("CONTRIBUTIONS FETCHED")
    print("================================")

    print(
        f"Days found       : {len(days)}"
    )

    print(
        f"Non-zero days    : "
        f"{sum(day['count'] > 0 for day in days)}"
    )

    print(
        f"Total            : "
        f"{stats['total_contributions']}"
    )

    print(
        f"Current streak   : "
        f"{stats['current_streak']}"
    )

    print(
        f"Longest streak   : "
        f"{stats['longest_streak']}"
    )

    print(
        f"Best day         : "
        f"{stats['best_day']}"
    )

    print(
        f"Saved to         : {OUTPUT}"
    )

    print("================================")


if __name__ == "__main__":
    main()