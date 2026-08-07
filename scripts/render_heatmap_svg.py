import json
from datetime import datetime
from pathlib import Path


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")


# ============================================================
# SETTINGS
# ============================================================

WIDTH = 860
HEIGHT = 185

CELL = 12
GAP = 4

LEFT = 38
TOP = 42

# GitHub-inspired contribution colors
PALETTE = [
    "#161b22",  # 0
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
    "#69f0a0",  # 5
]


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not INPUT.exists():

        raise FileNotFoundError(
            f"{INPUT} not found.\n"
            "Run fetch_contributions.py first."
        )

    return json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )


# ============================================================
# BUILD 53-WEEK CALENDAR
# ============================================================

def build_calendar(days):

    day_map = {
        day["date"]: day
        for day in days
    }

    ordered = sorted(
        days,
        key=lambda x: x["date"]
    )

    first_date = datetime.strptime(
        ordered[0]["date"],
        "%Y-%m-%d"
    ).date()

    last_date = datetime.strptime(
        ordered[-1]["date"],
        "%Y-%m-%d"
    ).date()

    # Move backwards to Sunday.
    first_sunday = (
        first_date.toordinal()
        - (
            (first_date.weekday() + 1) % 7
        )
    )

    first_sunday = datetime.fromordinal(
        first_sunday
    ).date()

    weeks = []

    current = first_sunday

    while current <= last_date:

        week = []

        for row in range(7):

            date_string = current.isoformat()

            week.append(
                day_map.get(
                    date_string,
                    {
                        "date": date_string,
                        "count": 0,
                        "level": 0,
                    }
                )
            )

            current = datetime.fromordinal(
                current.toordinal() + 1
            ).date()

        weeks.append(week)

    return weeks


# ============================================================
# MAIN
# ============================================================

def main():

    data = load_data()

    days = data["days"]

    stats = data["stats"]

    weeks = build_calendar(days)

    # Keep exactly the latest 53 weeks.
    weeks = weeks[-53:]

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

    .title {{
        fill: #c9d1d9;
        font-family:
            "Courier New",
            monospace;
        font-size: 14px;
        font-weight: bold;
    }}

    .label {{
        fill: #8b949e;
        font-family:
            "Courier New",
            monospace;
        font-size: 10px;
    }}

    .cell {{
        opacity: 0;

        animation:
            reveal
            0.35s
            cubic-bezier(.2,.8,.2,1)
            forwards;
    }}

    @keyframes reveal {{

        from {{
            opacity: 0;
            transform:
                translate(-5px, -5px);
        }}

        to {{
            opacity: 1;
            transform:
                translate(0, 0);
        }}

    }}

</style>


<!-- ===================================================== -->
<!-- BACKGROUND -->
<!-- ===================================================== -->

<rect
    width="100%"
    height="100%"
    rx="12"
    fill="#0d1117"
/>


<!-- ===================================================== -->
<!-- TITLE -->
<!-- ===================================================== -->

<text
    class="title"
    x="{LEFT}"
    y="20"
>
    {data["username"]} · contributions
</text>


<!-- ===================================================== -->
<!-- DAY LABELS -->
<!-- ===================================================== -->

<text
    class="label"
    x="2"
    y="{TOP + 12}"
>
    Mon
</text>

<text
    class="label"
    x="2"
    y="{TOP + 3 * (CELL + GAP) + 12}"
>
    Wed
</text>

<text
    class="label"
    x="2"
    y="{TOP + 5 * (CELL + GAP) + 12}"
>
    Fri
</text>

'''

    # ========================================================
    # MONTH LABELS
    # ========================================================

    previous_month = None

    for column, week in enumerate(weeks):

        first_day = week[0]["date"]

        try:

            date = datetime.strptime(
                first_day,
                "%Y-%m-%d"
            )

        except ValueError:

            continue

        month = date.strftime("%b")

        if month != previous_month:

            x = (
                LEFT
                + column * (CELL + GAP)
            )

            svg += f'''
<text
    class="label"
    x="{x}"
    y="36"
>
    {month}
</text>
'''

            previous_month = month

    # ========================================================
    # CONTRIBUTION CELLS
    # ========================================================

    cell_index = 0

    for column, week in enumerate(weeks):

        for row, day in enumerate(week):

            level = int(
                day.get(
                    "level",
                    0
                )
            )

            # GitHub normally uses 0-4.
            # Clamp safely.
            level = max(
                0,
                min(
                    level,
                    4
                )
            )

            x = (
                LEFT
                + column * (CELL + GAP)
            )

            y = (
                TOP
                + row * (CELL + GAP)
            )

            # Diagonal reveal.
            delay = (
                column * 0.018
                + row * 0.035
            )

            count = day.get(
                "count",
                0
            )

            date = day.get(
                "date",
                ""
            )

            svg += f'''
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{PALETTE[level]}"
    style="animation-delay:{delay:.3f}s"
>
    <title>
        {count} contributions on {date}
    </title>
</rect>
'''

            cell_index += 1

    # ========================================================
    # LEGEND
    # ========================================================

    legend_y = 147

    svg += '''
<text
    class="label"
    x="38"
    y="158"
>
    Less
</text>
'''

    for level, color in enumerate(
        PALETTE[:5]
    ):

        x = (
            68
            + level * (CELL + GAP)
        )

        svg += f'''
<rect
    x="{x}"
    y="{legend_y}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{color}"
/>
'''

    svg += '''
<text
    class="label"
    x="148"
    y="158"
>
    More
</text>
'''

    # ========================================================
    # STATISTICS
    # ========================================================

    total = stats.get(
        "total_contributions",
        0
    )

    current = stats.get(
        "current_streak",
        0
    )

    longest = stats.get(
        "longest_streak",
        0
    )

    svg += f'''
<text
    class="label"
    x="240"
    y="158"
>
    {total:,} contributions
</text>

<text
    class="label"
    x="450"
    y="158"
>
    current streak: {current}d
</text>

<text
    class="label"
    x="660"
    y="158"
>
    best streak: {longest}d
</text>

</svg>
'''

    # ========================================================
    # WRITE FILE
    # ========================================================

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("================================")
    print("HEATMAP SVG CREATED")
    print("================================")
    print(f"Output : {OUTPUT}")
    print(f"Weeks  : {len(weeks)}")
    print(f"Cells  : {cell_index}")
    print(f"Total  : {total}")
    print(f"Streak : {current} days")
    print(f"Best   : {longest} days")
    print("================================")


if __name__ == "__main__":
    main()