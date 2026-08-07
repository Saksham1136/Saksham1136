from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


INPUT = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else "source-photo.jpg"
)

OUTPUT = Path("source-prepped.png")


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Could not find photo: {INPUT}"
        )

    print(f"Reading {INPUT}...")

    image = Image.open(INPUT).convert("RGBA")

    print("Removing background...")

    foreground = remove(image)

    print("Adding white background...")

    background = Image.new(
        "RGBA",
        foreground.size,
        "white"
    )

    composited = Image.alpha_composite(
        background,
        foreground
    )

    rgb = composited.convert("RGB")

    print("Converting to grayscale...")

    img = np.array(rgb)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    print("Enhancing local contrast...")

    # clahe = cv2.createCLAHE(
    #     clipLimit=2.0,
    #     tileGridSize=(8, 8)
    # )

    # enhanced = clahe.apply(gray)

    # print("Reducing tiny details...")

    # enhanced = cv2.GaussianBlur(
    #     enhanced,
    #     (3, 3),
    #     0
    # )

    clahe = cv2.createCLAHE(
    clipLimit=3.0,
    tileGridSize=(8, 8)
)

enhanced = clahe.apply(gray)

# Stretch the tonal range.
low = np.percentile(enhanced, 5)
high = np.percentile(enhanced, 95)

enhanced = np.clip(
    (enhanced - low) * 255.0 / (high - low),
    0,
    255
).astype(np.uint8)

# Slight blur removes tiny photographic noise.
enhanced = cv2.GaussianBlur(
    enhanced,
    (3, 3),
    0
)

Image.fromarray(enhanced).save(OUTPUT)

print()
print("SUCCESS!")
print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()