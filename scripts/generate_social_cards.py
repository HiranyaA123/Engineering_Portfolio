from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "img" / "social"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630
PAPER = "#efede7"
SLATE = "#0e1b2e"
SLATE_RAISED = "#16273f"
RULE = "#2a3d58"
OXIDE = "#ff6b4e"
BLUE = "#8e98a6"
INK = "#f2f0ea"
QUIET = "#b4bcc7"


def font(name: str, size: int):
    choices = {
        "display": ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/Arial.ttf"],
        "body": ["C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/Arial.ttf"],
        "mono": ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/Arial.ttf"],
    }
    for candidate in choices[name]:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


DISPLAY = font("display", 66)
BODY = font("body", 28)
MONO = font("mono", 20)
MONO_SMALL = font("mono", 16)


def base():
    image = Image.new("RGB", (W, H), SLATE)
    draw = ImageDraw.Draw(image)
    draw.rectangle((38, 38, W - 38, H - 38), outline="#2a3d58", width=2)
    return image, draw


def footer(draw):
    draw.text((70, 564), "HIRANYA AGARWAL / ENGINEERING PORTFOLIO", font=MONO_SMALL, fill=QUIET)
    draw.text((1055, 564), "2026", font=MONO_SMALL, fill=OXIDE)


def headline(draw, sheet, category, title, subtitle):
    draw.rounded_rectangle((70, 68, 205, 112), radius=4, fill="#c4301c")
    draw.text((88, 79), f"PROJECT {sheet}", font=MONO_SMALL, fill=INK)
    draw.text((238, 80), category.upper(), font=MONO_SMALL, fill=BLUE)

    y = 154
    for line in wrap(title, 25):
        draw.text((70, y), line, font=DISPLAY, fill=INK)
        y += 72
    for line in wrap(subtitle, 62):
        draw.text((73, y + 12), line, font=BODY, fill=QUIET)
        y += 38


def photo_card(filename, source, sheet, category, title, subtitle, focal=(0.5, 0.5)):
    source_image = Image.open(ROOT / source).convert("RGB")
    image = ImageOps.fit(source_image, (W, H), method=Image.Resampling.LANCZOS, centering=focal)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(780):
        alpha = int(225 * (1 - x / 780) ** 1.5)
        od.line((x, 0, x, H), fill=(14, 27, 46, alpha))
    od.rectangle((0, 0, W, H), outline=(14, 27, 46, 180), width=20)
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)
    headline(draw, sheet, category, title, subtitle)
    footer(draw)
    image.save(OUT / filename, "JPEG", quality=88, optimize=True, progressive=True)


def technical_card(filename, sheet, category, title, subtitle, motif=None):
    """Typographic card for projects with no photograph yet: a large index
    number on the right, nothing pretending to be a drawing."""
    image, draw = base()
    index = sheet.split("/")[0]
    big = font("display", 300)
    width = draw.textlength(index, font=big)
    draw.text((W - 80 - width, 200), index, font=big, fill=OXIDE)
    headline(draw, sheet, category, title, subtitle)
    footer(draw)
    image.save(OUT / filename, "JPEG", quality=88, optimize=True, progressive=True)


photo_card(
    "portfolio.jpg", "assets/img/vex/worlds-pit-1600.jpg", "01-06", "Portfolio set",
    "I build things that have to work on the day.", "CentralPass, autonomous flight and championship robotics.", (0.58, 0.48)
)
photo_card(
    "centralpass.jpg", "assets/img/primo-firle/customer-site-1280.jpg", "01/06", "Hospitality platform",
    "CentralPass", "Direct ordering built to replace the marketplace apps.", (0.58, 0.48)
)
technical_card("adam-drone.jpg", "02/06", "Autonomy", "ADA2M autonomous drone", "A custom carbon fibre aircraft in flight testing.", "drone")
photo_card(
    "vex-over-under.jpg", "assets/img/vex/over-under-robot-1600.jpg", "03/06", "Robotics",
    "VEX Over Under", "Two national titles and the 2023-24 season Worlds Sportsmanship Award.", (0.62, 0.5)
)
technical_card("bluesat-ground-station.jpg", "04/06", "Space systems", "BlueSat ground station", "Mechanical interfaces for a CubeSat antenna pointing assembly.", "antenna")
technical_card("sculpt-showdown.jpg", "05/06", "Interactive systems", "Sculpt Showdown", "A real-time multiplayer voxel sculpting game.", "voxels")
technical_card("trading-platform.jpg", "06/06", "Software systems", "Day trading platform", "Backtesting and risk controls before live capital.", "trading")

print(f"Generated 7 social cards in {OUT}")
