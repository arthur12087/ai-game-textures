#!/usr/bin/env python3
"""Create visual tiling previews and heuristic edge/lighting diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError as exc:  # pragma: no cover - environment-dependent message
    raise SystemExit(
        "Pillow is required. Install it in the active Python environment with: "
        "python -m pip install Pillow"
    ) from exc


RESAMPLING = getattr(Image, "Resampling", Image)


def mean_rgb(image: Image.Image) -> list[float]:
    return [round(value / 255.0, 6) for value in ImageStat.Stat(image).mean[:3]]


def mean_luma(image: Image.Image) -> float:
    return ImageStat.Stat(image.convert("L")).mean[0] / 255.0


def edge_mismatch(image: Image.Image, axis: str) -> tuple[float, Image.Image]:
    width, height = image.size
    if axis == "x":
        first = image.crop((0, 0, 1, height))
        last = image.crop((width - 1, 0, width, height))
        diff = ImageChops.difference(first, last)
        preview = diff.resize((64, min(height, 1024)), RESAMPLING.NEAREST)
    else:
        first = image.crop((0, 0, width, 1))
        last = image.crop((0, height - 1, width, height))
        diff = ImageChops.difference(first, last)
        preview = diff.resize((min(width, 1024), 64), RESAMPLING.NEAREST)

    mismatch = sum(ImageStat.Stat(diff).mean[:3]) / (3.0 * 255.0)
    return mismatch, preview


def band_imbalance(image: Image.Image, axis: str, fraction: float = 0.08) -> float:
    width, height = image.size
    if axis == "x":
        band = max(1, int(width * fraction))
        first = image.crop((0, 0, band, height))
        last = image.crop((width - band, 0, width, height))
    else:
        band = max(1, int(height * fraction))
        first = image.crop((0, 0, width, band))
        last = image.crop((0, height - band, width, height))
    return abs(mean_luma(first) - mean_luma(last))


def half_imbalance(image: Image.Image, axis: str) -> float:
    width, height = image.size
    if axis == "x":
        first = image.crop((0, 0, width // 2, height))
        last = image.crop((width // 2, 0, width, height))
    else:
        first = image.crop((0, 0, width, height // 2))
        last = image.crop((0, height // 2, width, height))
    return abs(mean_luma(first) - mean_luma(last))


def label(value: float, low: float, high: float) -> str:
    if value <= low:
        return "low"
    if value <= high:
        return "moderate"
    return "high"


def make_tile_preview(image: Image.Image, count: int, max_tile_edge: int) -> Image.Image:
    scale = min(1.0, max_tile_edge / max(image.size))
    tile_size = (
        max(1, round(image.width * scale)),
        max(1, round(image.height * scale)),
    )
    tile = image.resize(tile_size, RESAMPLING.LANCZOS)
    preview = Image.new("RGB", (tile.width * count, tile.height * count))
    for y in range(count):
        for x in range(count):
            preview.paste(tile, (x * tile.width, y * tile.height))
    return preview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate 3x3/8x8 tiling previews and heuristic seam/lighting metrics. "
            "Metrics are diagnostic, not an automatic approval gate."
        )
    )
    parser.add_argument("image", type=Path, help="Texture image to inspect")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory; defaults to <image-stem>-validation beside the image",
    )
    parser.add_argument(
        "--preview-tile-edge",
        type=int,
        default=256,
        help="Maximum edge of one tile in mosaic previews (default: 256)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.image.is_file():
        print(f"Input image does not exist: {args.image}", file=sys.stderr)
        return 2
    if args.preview_tile_edge < 32:
        print("--preview-tile-edge must be at least 32", file=sys.stderr)
        return 2

    output = args.output or args.image.with_name(f"{args.image.stem}-validation")
    output.mkdir(parents=True, exist_ok=True)

    with Image.open(args.image) as opened:
        image = opened.convert("RGB")

    edge_x, edge_x_preview = edge_mismatch(image, "x")
    edge_y, edge_y_preview = edge_mismatch(image, "y")
    edge_x_preview.save(output / "edge-difference-left-right.png")
    edge_y_preview.save(output / "edge-difference-top-bottom.png")
    make_tile_preview(image, 3, args.preview_tile_edge).save(output / "tile-3x3.jpg", quality=92)
    make_tile_preview(image, 8, args.preview_tile_edge).save(output / "tile-8x8.jpg", quality=90)

    metrics = {
        "edge_pixel_mismatch": {
            "left_right": round(edge_x, 6),
            "top_bottom": round(edge_y, 6),
            "rating": label(max(edge_x, edge_y), 0.03, 0.08),
        },
        "edge_band_luma_imbalance": {
            "left_right": round(band_imbalance(image, "x"), 6),
            "top_bottom": round(band_imbalance(image, "y"), 6),
        },
        "half_image_luma_imbalance": {
            "left_right": round(half_imbalance(image, "x"), 6),
            "top_bottom": round(half_imbalance(image, "y"), 6),
        },
    }
    lighting_score = max(
        *metrics["edge_band_luma_imbalance"].values(),
        *metrics["half_image_luma_imbalance"].values(),
    )
    metrics["lighting_imbalance_rating"] = label(lighting_score, 0.02, 0.05)

    report = {
        "input": str(args.image.resolve()),
        "dimensions": {"width": image.width, "height": image.height},
        "mean_rgb_0_to_1": mean_rgb(image),
        "metrics": metrics,
        "interpretation": [
            "Ratings are heuristics, not pass/fail certification.",
            "Inspect tile-3x3.jpg for seams and tile-8x8.jpg for repeated focal marks or grids.",
            "Structured materials must also preserve joints; these scalar metrics cannot verify topology.",
            "Final approval requires testing the imported material on the target mesh and engine.",
        ],
    }
    report_path = output / "report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Validation artifacts: {output.resolve()}")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
