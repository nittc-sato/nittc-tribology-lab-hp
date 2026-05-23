"""Replace edge-connected dark backgrounds with white in research figures."""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

IMAGES = Path(__file__).resolve().parent.parent / "images"


def flood_background_mask(pixels, w: int, h: int, is_bg) -> list[list[bool]]:
    mask = [[False] * w for _ in range(h)]

    def flood(x: int, y: int) -> None:
        if mask[y][x] or not is_bg(*pixels[x, y]):
            return
        q = deque([(x, y)])
        mask[y][x] = True
        while q:
            cx, cy = q.popleft()
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < w and 0 <= ny < h and not mask[ny][nx]:
                    if is_bg(*pixels[nx, ny]):
                        mask[ny][nx] = True
                        q.append((nx, ny))

    for x in range(w):
        flood(x, 0)
        flood(x, h - 1)
    for y in range(h):
        flood(0, y)
        flood(w - 1, y)
    return mask


def black_bg_to_white(
    path_in: Path,
    path_out: Path,
    *,
    invert_white_text: bool = False,
    bg_max: int = 28,
    text_min: int = 242,
) -> None:
    im = Image.open(path_in).convert("RGB")
    w, h = im.size
    pixels = im.load()
    is_bg = lambda r, g, b: max(r, g, b) <= bg_max
    mask = flood_background_mask(pixels, w, h, is_bg)
    out = im.copy()
    op = out.load()
    for y in range(h):
        for x in range(w):
            if mask[y][x]:
                op[x, y] = (255, 255, 255)
            elif invert_white_text:
                r, g, b = pixels[x, y]
                if min(r, g, b) >= text_min and max(r, g, b) - min(r, g, b) <= 20:
                    op[x, y] = (30, 30, 30)
    out.save(path_out, quality=92)
    print(f"{path_out.name}: background pixels -> white: {sum(sum(row) for row in mask)}")


def main() -> None:
    black_bg_to_white(
        IMAGES / "research-additives-source.png",
        IMAGES / "research-additives.png",
    )
    tribo = IMAGES / "research-tribochemistry.png"
    black_bg_to_white(tribo, tribo, invert_white_text=True)


if __name__ == "__main__":
    main()
