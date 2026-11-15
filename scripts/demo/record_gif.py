"""Record the README demo GIF from a built demo page (real model output, real page script).

    uvx --from playwright==1.63.0 --with pillow python scripts/demo/record_gif.py \
        demo/flask.html docs/assets/demo.gif

Opens the static review page in headless Chromium, hovers checklist items (the page highlights
each item's source span), answers them, and writes an animated GIF. Nothing is mocked: the
page is the one published at https://professor3333.github.io/TriggerMap/. The pointer is drawn
onto the screenshots, because headless screenshots do not include one.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import Locator, Page, sync_playwright

VIEWPORT = {"width": 1280, "height": 800}
OUT_WIDTH = 1100
ANSWERS = ("Present", "Present", "Absent", "Unknown")  # one per checklist item, in order


def pointer(image: Image.Image, x: float, y: float) -> Image.Image:
    """Draw a mouse pointer with its tip at (x, y)."""
    shape = [(0, 0), (0, 21), (5, 16), (9, 25), (13, 23), (9, 15), (16, 15)]
    draw = ImageDraw.Draw(image)
    draw.polygon([(x + dx, y + dy) for dx, dy in shape], fill="#ffffff", outline="#0f172a")
    return image


def shot(page: Page, at: tuple[float, float] | None = None) -> Image.Image:
    image = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
    return pointer(image, *at) if at else image


def finish(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Scale a frame, frame it thinly (so a white page shows on a white README), and palettise."""
    image = image.resize(size, Image.Resampling.LANCZOS)
    ImageDraw.Draw(image).rectangle((0, 0, size[0] - 1, size[1] - 1), outline="#cbd5e1")
    return image.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)


def spot(target: Locator, right: float = 0.5, down: float = 0.5) -> dict[str, float]:
    """A position inside the target, as fractions of its box (used to hover and to draw)."""
    box = target.bounding_box()
    assert box is not None
    return {"x": box["width"] * right, "y": box["height"] * down}


def absolute(target: Locator, position: dict[str, float]) -> tuple[float, float]:
    box = target.bounding_box()
    assert box is not None
    return box["x"] + position["x"], box["y"] + position["y"]


def record(page_file: Path, out: Path) -> None:
    frames: list[tuple[Image.Image, int]] = []  # (image, milliseconds)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT, color_scheme="light", reduced_motion="reduce")
        page.goto(page_file.resolve().as_uri())
        frames.append((shot(page), 1800))
        items = page.locator(".item")
        for index in range(items.count()):
            item = items.nth(index)
            item.scroll_into_view_if_needed()
            surface = item.locator(".surface")
            beside = spot(surface, right=0.93)  # right of the quoted span, not on top of it
            surface.hover(position=beside)  # the page marks this item's span in the text
            page.wait_for_timeout(350)
            frames.append((shot(page, absolute(surface, beside)), 1300))
            answer = item.locator(".answers label", has_text=ANSWERS[index % len(ANSWERS)])
            low = spot(answer, down=0.8)  # keeps the answer's label readable
            answer.click(position=low)
            page.wait_for_timeout(200)
            frames.append((shot(page, absolute(answer, low)), 1100))
        export = page.locator("#export-md")
        export.scroll_into_view_if_needed()
        low = spot(export, down=0.8)
        export.hover(position=low)
        page.wait_for_timeout(200)
        frames.append((shot(page, absolute(export, low)), 2600))
        browser.close()

    height = round(VIEWPORT["height"] * OUT_WIDTH / VIEWPORT["width"])
    images = [finish(image, (OUT_WIDTH, height)) for image, _ in frames]
    out.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        out,
        save_all=True,
        append_images=images[1:],
        duration=[ms for _, ms in frames],
        loop=0,
        optimize=True,
    )
    print(f"wrote {out}: {len(images)} frames, {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    record(Path(sys.argv[1]), Path(sys.argv[2]))
