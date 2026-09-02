from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from datetime import date
import json
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
FOLDER_REDIRECTS = [ROOT / "projects" / "primo-firle" / "index.html"]
PUBLIC_HTML = [ROOT / "index.html", ROOT / "404.html"] + [
    page for page in sorted((ROOT / "projects").glob("*/index.html")) if page not in FOLDER_REDIRECTS
]


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.h1 = 0
        self.canonical = []
        self.description = []
        self.images = []
        self.json_ld = []
        self._json_ld = False
        self._json_buffer = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and values.get("href"):
            self.refs.append(("href", values["href"]))
        if tag in {"img", "script"} and values.get("src"):
            self.refs.append(("src", values["src"]))
        if tag == "link" and values.get("href"):
            self.refs.append(("href", values["href"]))
            if values.get("rel") == "canonical":
                self.canonical.append(values["href"])
        if tag == "meta" and values.get("name") == "description":
            self.description.append(values.get("content", ""))
        if tag == "img":
            self.images.append(values)
        if tag == "script" and values.get("type") == "application/ld+json":
            self._json_ld = True
            self._json_buffer = []

    def handle_data(self, data):
        if self._json_ld:
            self._json_buffer.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json_ld:
            self.json_ld.append("".join(self._json_buffer))
            self._json_ld = False


def resolve_local(page, ref):
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or ref.startswith("mailto:") or ref.startswith("tel:") or ref.startswith("#"):
        return None
    clean = parsed.path
    if not clean:
        return None
    project_prefix = "/Engineering_Portfolio/"
    if clean.startswith(project_prefix):
        clean = clean[len(project_prefix):]
        target = (ROOT / clean).resolve()
    else:
        target = (page.parent / clean).resolve()
    if clean.endswith("/"):
        target = target / "index.html"
    return target


errors = []
canonical_urls = []
for page in PUBLIC_HTML:
    parser = AuditParser()
    parser.feed(page.read_text(encoding="utf-8"))
    label = page.relative_to(ROOT)

    if parser.h1 != 1:
        errors.append(f"{label}: expected one h1, found {parser.h1}")
    if len(parser.ids) != len(set(parser.ids)):
        errors.append(f"{label}: duplicate id values")
    if page.name == "index.html" and len(parser.canonical) != 1:
        errors.append(f"{label}: expected one canonical URL")
    if page != ROOT / "404.html" and len(parser.canonical) == 1:
        canonical_urls.append(parser.canonical[0])
    if page.name == "index.html" and len(parser.description) != 1:
        errors.append(f"{label}: expected one meta description")
    if parser.description and len(parser.description[0]) > 160:
        errors.append(f"{label}: meta description is {len(parser.description[0])} characters")
    if page != ROOT / "404.html" and not parser.json_ld:
        errors.append(f"{label}: missing JSON-LD")

    for payload in parser.json_ld:
        try:
            json.loads(payload)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: invalid JSON-LD ({exc})")

    for image in parser.images:
        for required in ("src", "alt", "width", "height"):
            if required not in image:
                errors.append(f"{label}: image missing {required}")

    for attribute, ref in parser.refs:
        target = resolve_local(page, ref)
        if target is None:
            continue
        if not target.exists():
            errors.append(f"{label}: broken {attribute} {ref}")

sitemap = ROOT / "sitemap.xml"
try:
    tree = ET.parse(sitemap)
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [node.text for node in tree.findall("s:url/s:loc", namespace)]
    modified = [node.text for node in tree.findall("s:url/s:lastmod", namespace)]
    if len(locations) != len(set(locations)):
        errors.append("sitemap.xml: duplicate URLs")
    if len(locations) != 7:
        errors.append(f"sitemap.xml: expected 7 public URLs, found {len(locations)}")
    if len(modified) != len(locations):
        errors.append("sitemap.xml: every URL must include lastmod")
    if set(locations) != set(canonical_urls):
        errors.append("sitemap.xml: URLs do not match public page canonicals")
    for value in modified:
        try:
            date.fromisoformat(value)
        except (TypeError, ValueError):
            errors.append(f"sitemap.xml: invalid lastmod {value}")
except (ET.ParseError, OSError) as exc:
    errors.append(f"sitemap.xml: {exc}")

legacy = sorted((ROOT / "projects").glob("*.html")) + FOLDER_REDIRECTS
for page in legacy:
    text = page.read_text(encoding="utf-8")
    if 'name="robots" content="noindex"' not in text or 'rel="canonical"' not in text or "location.replace" not in text:
        errors.append(f"{page.relative_to(ROOT)}: incomplete legacy redirect shim")

if errors:
    print("Site validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"Validated {len(PUBLIC_HTML)} public HTML pages, {len(legacy)} legacy redirects and the sitemap.")
