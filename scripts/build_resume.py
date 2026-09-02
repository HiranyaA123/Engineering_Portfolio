from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "docs" / "Hiranya-Agarwal-Resume.pdf"

PAGE_W, PAGE_H = A4
MARGIN_X = 38
TOP = PAGE_H - 34
INK = HexColor("#14181a")
MID = HexColor("#3c464b")
BLUE = HexColor("#1b4e7d")
OXIDE = HexColor("#a63a17")
RULE = HexColor("#b7bcaf")


def split_lines(text, font, size, width):
    words = text.split()
    lines, line = [], []
    for word in words:
        candidate = " ".join(line + [word])
        if line and stringWidth(candidate, font, size) > width:
            lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    return lines


def draw_link(c, x, y, label, url, font="Helvetica", size=8.1, colour=MID):
    c.setFont(font, size)
    c.setFillColor(colour)
    c.drawString(x, y, label)
    width = stringWidth(label, font, size)
    c.linkURL(url, (x, y - 2, x + width, y + size + 1), relative=0)
    return width


def section(c, title, y):
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(MARGIN_X, y + 5, PAGE_W - MARGIN_X, y + 5)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(BLUE)
    c.drawString(MARGIN_X, y - 9, title.upper())
    return y - 24


def role(c, title, organisation, dates, y, bullets, width=PAGE_W - 2 * MARGIN_X):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN_X, y, title)
    title_w = stringWidth(title, "Helvetica-Bold", 10)
    c.setFont("Helvetica", 9.3)
    c.setFillColor(MID)
    c.drawString(MARGIN_X + title_w + 5, y, f"|  {organisation}")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(OXIDE)
    c.drawRightString(PAGE_W - MARGIN_X, y, dates)
    y -= 14
    for bullet in bullets:
        lines = split_lines(bullet, "Helvetica", 9, width - 15)
        c.setFillColor(MID)
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN_X + 2, y, "-")
        for i, line in enumerate(lines):
            c.drawString(MARGIN_X + 11, y, line)
            if i < len(lines) - 1:
                y -= 11.5
        y -= 13
    return y + 2


c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
c.setTitle("Hiranya Agarwal - Engineering Resume")
c.setAuthor("Hiranya Agarwal")
c.setSubject("Mechanical engineering, robotics, autonomous systems and software")
c.setCreator("Hiranya Agarwal engineering portfolio")

y = TOP
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 21)
c.drawString(MARGIN_X, y, "HIRANYA AGARWAL")
c.setFont("Helvetica", 8.5)
c.setFillColor(BLUE)
c.drawRightString(PAGE_W - MARGIN_X, y + 2, "MECHANICAL ENGINEERING / ROBOTICS / AUTONOMOUS SYSTEMS")

y -= 18
x = MARGIN_X
c.setFont("Helvetica", 8.1)
c.setFillColor(MID)
c.drawString(x, y, "Sydney, NSW")
x += stringWidth("Sydney, NSW", "Helvetica", 8.1) + 12
c.drawString(x, y, "|  0452 145 196  |")
x += stringWidth("|  0452 145 196  |", "Helvetica", 8.1) + 7
x += draw_link(c, x, y, "agarwalhiranya@gmail.com", "mailto:agarwalhiranya@gmail.com") + 7
c.drawString(x, y, "|")
x += 9
x += draw_link(c, x, y, "LinkedIn", "https://linkedin.com/in/hiranyaagarwal", colour=BLUE) + 9
x += draw_link(c, x, y, "GitHub", "https://github.com/HiranyaA123", colour=BLUE)

y = section(c, "Education", y - 9)
c.setFont("Helvetica-Bold", 9.8)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "Bachelor of Engineering (Honours), Mechanical Engineering")
c.setFont("Helvetica", 9.2)
c.setFillColor(MID)
c.drawString(MARGIN_X + 286, y, "|  UNSW Sydney")
c.setFillColor(OXIDE)
c.setFont("Helvetica-Bold", 9)
c.drawRightString(PAGE_W - MARGIN_X, y, "2025 - 2028 (expected)")
y -= 16
c.setFont("Helvetica-Bold", 9.6)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "SACE")
c.setFont("Helvetica", 9.1)
c.setFillColor(MID)
c.drawString(MARGIN_X + 29, y, "|  Pedare Christian College, Golden Grove SA  |  ATAR: 97.05")
c.setFillColor(OXIDE)
c.setFont("Helvetica-Bold", 9)
c.drawRightString(PAGE_W - MARGIN_X, y, "2024")

y = section(c, "Technical skills", y - 10)
skills = [
    ("CAD and mechanical design", "SolidWorks, Fusion 360; drone airframes, competition robots, antenna mounts and brackets"),
    ("Programming", "C++ for embedded and competition robotics; Python for automation, data analysis and trading APIs; MATLAB; TypeScript"),
    ("Mechatronics and embedded", "IMUs, encoders, colour and environmental sensors; flight controllers; pneumatics; Raspberry Pi and ADC acquisition"),
]
for label, detail in skills:
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(INK)
    c.drawString(MARGIN_X, y, label + ":")
    offset = stringWidth(label + ":", "Helvetica-Bold", 9) + 5
    c.setFont("Helvetica", 9)
    c.setFillColor(MID)
    first_width = PAGE_W - 2 * MARGIN_X - offset
    lines = split_lines(detail, "Helvetica", 9, first_width)
    for i, line in enumerate(lines):
        c.drawString(MARGIN_X + offset, y, line)
        if i < len(lines) - 1:
            y -= 11
    y -= 15

y = section(c, "Experience", y - 2)
y = role(c, "Co-Founder and CFO", "Project Umbrella Labs, UNSW", "2025 - Present", y, [
    "Co-founded a student-led research and development lab running practical engineering projects across autonomous UAVs, neural interfaces and agricultural monitoring."
])
y = role(c, "VEX Robotics Mentor (Casual)", "Barker College, Hornsby NSW", "2026 - Present", y, [
    "Coach VEX IQ teams through design, build and programming cycles using national-championship VRC competition experience."
])
y = role(c, "Mechanical Lead", "BlueSat UNSW CubeSat Program", "Feb - Dec 2025", y, [
    "Led mechanical design of the ground-station antenna pointing mounts and bracketry, coordinating interfaces across electrical, software and mechanical subteams.",
    "Handed the mechanical package to the team while the ground station remained in development."
])
y = role(c, "Front of House", "Caffe Primo, Munno Para SA", "Dec 2021 - Jan 2025", y, [
    "Handled orders, payments and bar service in a high-volume hospitality environment."
])

y = section(c, "Selected projects", y - 2)
y = role(c, "Cafe Primo Firle restaurant platform", "Working restaurant", "2026 - Present", y, [
    "Built and operate a production platform connecting customer ordering, Stripe checkout, live staff and admin dashboards, PostgreSQL, Socket.io updates and ESC/POS receipt printing."
])
y = role(c, "ADA2M autonomous agricultural drone", "Project Umbrella Labs, team of two", "2025 - Present", y, [
    "Designed a custom carbon-fibre airframe around a SpeedyBee F405 flight controller, TBS Crossfire link, Jetson Nano and environmental sensor payload; currently in flight testing."
])
y = role(c, "Automated day-trading platform", "Personal project", "2025 - Present", y, [
    "Building a modular Python system on the Interactive Brokers API with backtesting, position sizing, stop-loss logic and drawdown limits; no live performance claim."
])

y = section(c, "Leadership, awards and service", y - 2)
y = role(c, "Captain and Lead Programmer", "VEX Robotics Team 41103A", "2018 - 2024", y, [
    "Led a seven-person team to back-to-back Australian National Championships, two World Championship qualifications and the 2024 Worlds Sportsmanship Award in Dallas.",
    "Wrote autonomous and driver-control C++ using IMU, colour-sensor and encoder data; designed pneumatic intake, scoring and elevation mechanisms."
])
y = role(c, "Volunteer", "Little Sisters of the Poor and Order of Malta outreach", "2024 - Present", y, [
    "Make weekly maintenance and companionship visits with elderly residents and distribute essential supplies through organised Sydney street outreach."
])

y = section(c, "Recognition", y - 2)
c.setFont("Helvetica", 8.8)
c.setFillColor(MID)
c.drawString(MARGIN_X, y, "Australian Defence Force Future Innovators Award (2024)")
c.drawString(MARGIN_X, y - 13, "Tournament Excellence, Australian National VEX Championship (2023)")
c.drawString(MARGIN_X, y - 26, "Robotics work featured by ABC Radio Adelaide, Life FM and Glam Adelaide")

c.setStrokeColor(RULE)
c.line(MARGIN_X, 33, PAGE_W - MARGIN_X, 33)
c.setFont("Helvetica", 7.6)
c.setFillColor(MID)
c.drawString(MARGIN_X, 20, "References available on request")
c.drawRightString(PAGE_W - MARGIN_X, 20, "hiranyaa123.github.io/Engineering_Portfolio/")
c.linkURL("https://hiranyaa123.github.io/Engineering_Portfolio/", (PAGE_W - 210, 17, PAGE_W - MARGIN_X, 30), relative=0)

c.showPage()
c.save()
print(f"Built {OUTPUT}")
