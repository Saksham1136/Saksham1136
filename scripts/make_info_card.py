from pathlib import Path

OUTPUT = Path("info-card.svg")


# ============================================================
# YOUR PROFILE
# ============================================================

USERNAME = "Saksham1136"
NAME = "Saksham Kumar"

ROLE = "AI/ML & Generative AI Developer"

CURRENTLY = "Building Agentic AI & RAG systems"

FOCUS_LINE_1 = "LangGraph · multimodal RAG"
FOCUS_LINE_2 = "LLM orchestration"

STACK = "Python · LangGraph · RAG · LLMs"

HIGHLIGHTS = [
    "Agentic AI & LLM orchestration",
    "Multimodal RAG systems",
    "Intelligent data-driven applications",
]

LINKEDIN = "linkedin.com/in/saksham-kumar-66b410264"


# ============================================================
# SVG SETTINGS
# ============================================================

WIDTH = 490
HEIGHT = 390

BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
BLUE = "#58a6ff"


# ============================================================
# ESCAPE XML SPECIAL CHARACTERS
# ============================================================

def escape(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


# ============================================================
# MAIN
# ============================================================

def main():

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="12"
    fill="{BG}"
    stroke="{BORDER}"
    stroke-width="2"
/>

<style>

    .terminal {{
        font-family:
            "Courier New",
            "Liberation Mono",
            monospace;
    }}

    .title {{
        fill: {TEXT};
        font-size: 15px;
        font-weight: bold;
    }}

    .key {{
        fill: {GREEN};
        font-size: 14px;
        font-weight: bold;
    }}

    .value {{
        fill: {TEXT};
        font-size: 14px;
    }}

    .muted {{
        fill: {MUTED};
        font-size: 12px;
    }}

    .highlight {{
        fill: {BLUE};
        font-size: 13px;
    }}

    .line {{
        opacity: 0;

        animation:
            appear 0.45s ease-out
            forwards;
    }}

    @keyframes appear {{

        from {{
            opacity: 0;
            transform: translateX(-10px);
        }}

        to {{
            opacity: 1;
            transform: translateX(0);
        }}

    }}

</style>


<!-- ================================================== -->
<!-- TERMINAL TITLE BAR -->
<!-- ================================================== -->

<circle
    cx="20"
    cy="20"
    r="5"
    fill="#ff5f56"
/>

<circle
    cx="38"
    cy="20"
    r="5"
    fill="#ffbd2e"
/>

<circle
    cx="56"
    cy="20"
    r="5"
    fill="#27c93f"
/>

<text
    class="terminal title"
    x="78"
    y="25"
>{escape(USERNAME)}@github:~</text>


<!-- ================================================== -->
<!-- COMMAND -->
<!-- Animation delay: 0.15s -->
<!-- ================================================== -->

<text
    class="terminal muted line"
    x="25"
    y="65"
    style="animation-delay:0.15s"
>$ neofetch</text>


<!-- ================================================== -->
<!-- USER -->
<!-- Animation delay: 0.30s -->
<!-- ================================================== -->

<text
    class="terminal key line"
    x="25"
    y="105"
    style="animation-delay:0.30s"
>user</text>

<text
    class="terminal value line"
    x="145"
    y="105"
    style="animation-delay:0.30s"
>{escape(USERNAME)}</text>


<!-- ================================================== -->
<!-- ROLE -->
<!-- Animation delay: 0.40s -->
<!-- ================================================== -->

<text
    class="terminal key line"
    x="25"
    y="135"
    style="animation-delay:0.40s"
>role</text>

<text
    class="terminal value line"
    x="145"
    y="135"
    style="animation-delay:0.40s"
>{escape(ROLE)}</text>


<!-- ================================================== -->
<!-- CURRENTLY -->
<!-- Animation delay: 0.50s -->
<!-- ================================================== -->

<text
    class="terminal key line"
    x="25"
    y="165"
    style="animation-delay:0.50s"
>now</text>

<text
    class="terminal value line"
    x="145"
    y="165"
    style="animation-delay:0.50s"
>{escape(CURRENTLY)}</text>


<!-- ================================================== -->
<!-- FOCUS -->
<!-- Animation delay: 0.60s -->
<!-- ================================================== -->

<text
    class="terminal key line"
    x="25"
    y="195"
    style="animation-delay:0.60s"
>focus</text>

<text
    class="terminal value line"
    x="145"
    y="195"
    style="animation-delay:0.60s"
>{escape(FOCUS_LINE_1)}</text>

<text
    class="terminal value line"
    x="145"
    y="215"
    style="animation-delay:0.60s"
>{escape(FOCUS_LINE_2)}</text>


<!-- ================================================== -->
<!-- STACK -->
<!-- Animation delay: 0.70s -->
<!-- ================================================== -->

<text
    class="terminal key line"
    x="25"
    y="245"
    style="animation-delay:0.70s"
>stack</text>

<text
    class="terminal value line"
    x="145"
    y="245"
    style="animation-delay:0.70s"
>{escape(STACK)}</text>


<!-- ================================================== -->
<!-- HIGHLIGHTS -->
<!-- Animation delays: 0.80s, 0.90s, 1.00s -->
<!-- ================================================== -->

<text
    class="terminal highlight line"
    x="25"
    y="285"
    style="animation-delay:0.80s"
>→ {escape(HIGHLIGHTS[0])}</text>

<text
    class="terminal highlight line"
    x="25"
    y="310"
    style="animation-delay:0.90s"
>→ {escape(HIGHLIGHTS[1])}</text>

<text
    class="terminal highlight line"
    x="25"
    y="335"
    style="animation-delay:1.00s"
>→ {escape(HIGHLIGHTS[2])}</text>


<!-- ================================================== -->
<!-- FOOTER -->
<!-- ================================================== -->

<text
    class="terminal muted"
    x="25"
    y="365"
>github.com/Saksham1136</text>

<text
    class="terminal muted"
    x="25"
    y="382"
>{escape(LINKEDIN)}</text>


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
    print("INFO CARD CREATED")
    print("================================")
    print(f"Output: {OUTPUT}")
    print(f"Size  : {WIDTH} × {HEIGHT}")
    print("Animation delays:")
    print("  command    0.15s")
    print("  user       0.30s")
    print("  role       0.40s")
    print("  now        0.50s")
    print("  focus      0.60s")
    print("  stack      0.70s")
    print("  highlights 0.80s → 1.00s")
    print("================================")


if __name__ == "__main__":
    main()