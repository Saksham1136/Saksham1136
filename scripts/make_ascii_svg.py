# from pathlib import Path
# from PIL import Image
# from xml.sax.saxutils import escape


# INPUT = Path("source-prepped.png")
# OUTPUT = Path("avi-ascii.svg")

# # ASCII resolution.
# # Increase this for more detail.
# WIDTH = 130

# # Characters from light → dark.
# # RAMP = " .`:-=+*cs#%@"
# # RAMP = "  .,:;irsXA253hMHGS#9B&@"
# # RAMP = "    ..::--==++**##%%@@"
# RAMP = " .:-=+*#%@"

# FONT_SIZE = 6
# CHAR_WIDTH = 5.5
# LINE_HEIGHT = 7.0


# def brightness_to_char(value):
#     index = int(value / 256 * len(RAMP))
#     index = min(index, len(RAMP) - 1)
#     return RAMP[index]


# def main():
#     if not INPUT.exists():
#         raise FileNotFoundError(
#             f"Could not find {INPUT}"
#         )

#     print(f"Reading {INPUT}...")

#     image = Image.open(INPUT).convert("L")

#     # Characters are taller than they are wide,
#     # so compensate for terminal character proportions.
#     aspect_ratio = image.height / image.width
#     height = max(
#         1,
#         int(WIDTH * aspect_ratio * 0.50)
#     )

#     image = image.resize(
#         (WIDTH, height),
#         Image.Resampling.LANCZOS
#     )

#     svg_width = WIDTH * CHAR_WIDTH
#     svg_height = height * LINE_HEIGHT

#     rows = []

#     for y in range(height):
#         row = []

#         for x in range(WIDTH):
#             brightness = image.getpixel((x, y))
#             row.append(
#                 brightness_to_char(brightness)
#             )

#         rows.append("".join(row))

#     svg = f'''<svg
#     xmlns="http://www.w3.org/2000/svg"
#     width="{svg_width}"
#     height="{svg_height}"
#     viewBox="0 0 {svg_width} {svg_height}">

#     <rect
#         width="100%"
#         height="100%"
#         fill="white"
#     />

#     <style>
#         .ascii {{
#             font-family: monospace;
#             font-size: {FONT_SIZE}px;
#             fill: #8b949e;
#             font-weight: 400;
#         }}

#         .row {{
#             opacity: 0;
#             animation:
#                 reveal 0.55s ease-out forwards;
#         }}

#         @keyframes reveal {{
#             from {{
#                 opacity: 0;
#                 transform: translateX(-12px);
#             }}

#             to {{
#                 opacity: 1;
#                 transform: translateX(0);
#             }}
#         }}
#     </style>
# '''

#     for y, row in enumerate(rows):

#         # Escape characters for valid XML.
#         row = escape(row)

#         delay = y * 0.035

#         svg += f'''
#     <text
#         class="ascii row"
#         x="0"
#         y="{(y + 1) * LINE_HEIGHT}"
#         style="animation-delay: {delay:.3f}s"
#     >{row}</text>
# '''

#     svg += "\n</svg>\n"

#     OUTPUT.write_text(
#         svg,
#         encoding="utf-8"
#     )

#     print()
#     print("SUCCESS!")
#     print(f"Created: {OUTPUT}")
#     print(f"Grid: {WIDTH} columns × {height} rows")


# if __name__ == "__main__":
#     main()





# from pathlib import Path

# import numpy as np
# from PIL import Image
# from xml.sax.saxutils import escape


# INPUT = Path("source-prepped.png")
# OUTPUT = Path("avi-ascii.svg")

# # More characters = more facial detail.
# WIDTH = 200

# # Carefully tuned for portrait photography.
# # Bright -> dark
# # RAMP = "  .,:;irsXA253hMHGS#9B&@"

# # FONT_SIZE = 5.5
# # CHAR_WIDTH = 5.2
# # LINE_HEIGHT = 6.5


# RAMP = " .:-=+*#%@"

# FONT_SIZE = 7
# CHAR_WIDTH = 5.5
# LINE_HEIGHT = 7.0


# def brightness_to_char(value):
#     """
#     Convert brightness (0 = black, 255 = white)
#     into an ASCII character.

#     Gamma adjustment gives the mid-tones more room,
#     which is important for faces.
#     """

#     normalized = value / 255.0

#     # Make midtones slightly darker.
#     adjusted = normalized ** 0.82

#     index = int(
#         (1.0 - adjusted) * (len(RAMP) - 1)
#     )

#     index = max(0, min(index, len(RAMP) - 1))

#     return RAMP[index]


# def crop_image(image):
#     """
#     Remove some of the unnecessary white space
#     around the portrait.
#     """

#     array = np.array(image)

#     # Anything darker than this is considered
#     # part of the subject.
#     mask = array < 245

#     ys, xs = np.where(mask)

#     if len(xs) == 0:
#         return image

#     left = xs.min()
#     right = xs.max()
#     top = ys.min()
#     bottom = ys.max()

#     width = right - left
#     height = bottom - top

#     # Add a small margin around the subject.
#     margin_x = int(width * 0.06)
#     margin_y = int(height * 0.06)

#     left = max(0, left - margin_x)
#     right = min(image.width, right + margin_x)

#     top = max(0, top - margin_y)
#     bottom = min(image.height, bottom + margin_y)

#     return image.crop(
#         (left, top, right, bottom)
#     )


# def main():

#     if not INPUT.exists():
#         raise FileNotFoundError(
#             f"Could not find {INPUT}"
#         )

#     print(f"Reading {INPUT}...")

#     image = Image.open(INPUT).convert("L")

#     print("Cropping empty background...")

#     image = crop_image(image)

#     print("Resizing for ASCII...")

#     aspect_ratio = image.height / image.width

#     height = max(
#         1,
#         int(
#             WIDTH
#             * aspect_ratio
#             * 0.48
#         )
#     )

#     image = image.resize(
#         (WIDTH, height),
#         Image.Resampling.LANCZOS
#     )

#     pixels = np.array(image)

#     svg_width = WIDTH * CHAR_WIDTH
#     svg_height = height * LINE_HEIGHT

#     svg = f'''<svg
#     xmlns="http://www.w3.org/2000/svg"
#     width="{svg_width}"
#     height="{svg_height}"
#     viewBox="0 0 {svg_width} {svg_height}">

#     <rect
#         width="100%"
#         height="100%"
#         fill="white"
#     />

#     <style>

#         .ascii {{
#             font-family:
#                 "Courier New",
#                 "Liberation Mono",
#                 monospace;

#             font-size: {FONT_SIZE}px;
#             fill: #30363d;
#             font-weight: 400;

#             letter-spacing: 0;
#         }}

#         .row {{
#             opacity: 1;
#             transform: translateX(-10px);

#             animation:
#                 reveal 0.42s
#                 cubic-bezier(.2,.8,.2,1)
#                 forwards;
#         }}

#     </style>
# '''

#     for y in range(height):

#         characters = []

#         for x in range(WIDTH):

#             value = int(
#                 pixels[y, x]
#             )

#             character = (
#                 brightness_to_char(value)
#             )

#             characters.append(character)

#         row = escape(
#             "".join(characters)
#         )

#         delay = y * 0.025

#         svg += f'''
#     <text
#         class="ascii row"
#         x="0"
#         y="{(y + 1) * LINE_HEIGHT}"
#         style="animation-delay:{delay:.3f}s"
#     >{row}</text>
# '''

#     svg += """
# </svg>
# """

#     OUTPUT.write_text(
#         svg,
#         encoding="utf-8"
#     )

#     print()
#     print("SUCCESS!")
#     print(f"Created: {OUTPUT}")
#     print(
#         f"Grid: {WIDTH} × {height}"
#     )


# if __name__ == "__main__":
#     main()








from pathlib import Path

import numpy as np
from PIL import Image
from xml.sax.saxutils import escape


INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

# Final portrait resolution.
WIDTH = 200

# Bright -> dark.
RAMP = " .:-=+*#%@"

FONT_SIZE = 7
CHAR_WIDTH = 5.5
LINE_HEIGHT = 7.0


def brightness_to_char(value):
    """
    Convert grayscale brightness to an ASCII character.
    White becomes a space, black becomes @.
    """

    normalized = value / 255.0

    # Slightly emphasize facial midtones.
    adjusted = normalized ** 0.82

    index = int(
        (1.0 - adjusted) * (len(RAMP) - 1)
    )

    return RAMP[
        max(0, min(index, len(RAMP) - 1))
    ]


def crop_image(image):
    """
    Remove unnecessary white space around
    the actual portrait.
    """

    array = np.array(image)

    mask = array < 245

    ys, xs = np.where(mask)

    if len(xs) == 0:
        return image

    left = int(xs.min())
    right = int(xs.max())
    top = int(ys.min())
    bottom = int(ys.max())

    width = right - left
    height = bottom - top

    margin_x = int(width * 0.05)
    margin_y = int(height * 0.05)

    left = max(0, left - margin_x)
    right = min(image.width, right + margin_x)

    top = max(0, top - margin_y)
    bottom = min(image.height, bottom + margin_y)

    return image.crop(
        (left, top, right, bottom)
    )


def main():

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT}"
        )

    print(f"Reading {INPUT}...")

    image = Image.open(INPUT).convert("L")

    print("Cropping portrait...")

    image = crop_image(image)

    print("Resizing for ASCII...")

    aspect_ratio = image.height / image.width

    height = max(
        1,
        int(WIDTH * aspect_ratio * 0.48)
    )

    image = image.resize(
        (WIDTH, height),
        Image.Resampling.LANCZOS
    )

    pixels = np.array(image)

    svg_width = WIDTH * CHAR_WIDTH
    svg_height = height * LINE_HEIGHT

    # Center the text horizontally.
    center_x = svg_width / 2

    svg = f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{svg_width}"
    height="{svg_height}"
    viewBox="0 0 {svg_width} {svg_height}">

    <rect
        width="100%"
        height="100%"
        fill="white"
    />

    <style>

        .ascii {{
            font-family:
                "Courier New",
                "Liberation Mono",
                monospace;

            font-size: {FONT_SIZE}px;
            fill: #30363d;
            font-weight: 400;
            letter-spacing: 0;

            /* Keep the final portrait visible. */
            opacity: 1;
        }}

        /*
         * The rows start visible, then a clipping
         * rectangle reveals each row from left
         * to right.
         *
         * This means the final SVG remains visible
         * even after the animation finishes.
         */

        .reveal {{
            animation:
                wipe 0.55s
                cubic-bezier(.2,.8,.2,1)
                forwards;
        }}

        @keyframes wipe {{

            from {{
                width: 0;
            }}

            to {{
                width: {svg_width}px;
            }}

        }}

    </style>
'''

    for y in range(height):

        characters = []

        for x in range(WIDTH):

            value = int(pixels[y, x])

            character = brightness_to_char(
                value
            )

            characters.append(character)

        row = escape(
            "".join(characters)
        )

        y_position = (
            (y + 1) * LINE_HEIGHT
        )

        delay = y * 0.025

        clip_id = f"rowClip{y}"

        svg += f'''
    <clipPath id="{clip_id}">
        <rect
            class="reveal"
            x="0"
            y="{y * LINE_HEIGHT}"
            width="{svg_width}"
            height="{LINE_HEIGHT + 2}"
            style="animation-delay:{delay:.3f}s"
        />
    </clipPath>

    <text
        class="ascii"
        x="{center_x}"
        y="{y_position}"
        text-anchor="middle"
        clip-path="url(#{clip_id})"
    >{row}</text>
'''

    svg += """
</svg>
"""

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("================================")
    print("ASCII PORTRAIT CREATED")
    print("================================")
    print(f"Output : {OUTPUT}")
    print(f"Width  : {WIDTH} characters")
    print(f"Rows   : {height}")
    print(f"SVG    : {svg_width:.0f} × {svg_height:.0f}")
    print("Animation: row-by-row reveal")
    print("================================")


if __name__ == "__main__":
    main()