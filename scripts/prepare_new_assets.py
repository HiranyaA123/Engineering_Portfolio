"""Create public, metadata-free image variants; preserve all supplied originals."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("F5A0F884-3E14-41C2-A709-AF18608EB3B2.JPG", "drone/airframe", (600, 1000)),
    ("536E8210-2C2C-4E73-B38F-2C7000EB3BC8.JPG", "drone/bench-build", (600, 1000)),
    ("IMG_4909.jpeg", "portrait/studio", (500,)),
]

for source, slug, widths in SOURCES:
    with Image.open(ROOT / "assets/new" / source) as raw:
        image = ImageOps.exif_transpose(raw).convert("RGB")
        for width in widths:
            width = min(width, image.width)
            target = ROOT / "assets/img" / f"{slug}-{width}.jpg"
            target.parent.mkdir(parents=True, exist_ok=True)
            resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
            resized.save(target, "JPEG", quality=82, optimize=True, progressive=True)
            print(f"{target.relative_to(ROOT)}: {target.stat().st_size:,} bytes")
