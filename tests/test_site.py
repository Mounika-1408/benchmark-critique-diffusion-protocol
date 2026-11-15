from __future__ import annotations

import hashlib
import re
import struct
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest

DOCS = "docs"
CANONICAL = "https://p-r-e-m-i-u-m.github.io/benchmark-critique-diffusion-protocol/"
REPO = "https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.ids: list[str] = []
        self.text_parts: list[str] = []
        self.script_srcs: list[str] = []
        self.inline_scripts: list[tuple[str | None, str]] = []
        self._script_attrs: dict[str, str] | None = None
        self._script_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        self.tags.append((tag, values))
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "script":
            self._script_attrs = values
            self._script_text = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        self.tags.append((tag, values))
        if values.get("id"):
            self.ids.append(values["id"])

    def handle_data(self, data: str) -> None:
        if self._script_attrs is not None:
            self._script_text.append(data)
        else:
            self.text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script_attrs is not None:
            src = self._script_attrs.get("src")
            if src:
                self.script_srcs.append(src)
            else:
                self.inline_scripts.append((self._script_attrs.get("type"), "".join(self._script_text)))
            self._script_attrs = None

    def attr(self, tag: str, key: str) -> list[str]:
        return [values[key] for name, values in self.tags if name == tag and key in values]

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.text_parts)).strip()


@pytest.fixture(scope="module")
def site(root: Path) -> tuple[str, SiteParser]:
    html = (root / DOCS / "index.html").read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)
    parser.close()
    return html, parser


def test_site_files_exist(root: Path):
    docs = root / DOCS
    required = [
        "index.html",
        "styles.css",
        "site.js",
        "cite.bib",
        "404.html",
        "robots.txt",
        "sitemap.xml",
        ".nojekyll",
        "assets/favicon.svg",
        "assets/social-card.png",
        "assets/fonts/newsreader-latin.woff2",
        "assets/fonts/newsreader-latin-italic.woff2",
        "assets/fonts/ibm-plex-sans-latin.woff2",
        "assets/fonts/LICENSE-Newsreader.txt",
        "assets/fonts/LICENSE-IBMPlexSans.txt",
        "assets/figures/fig1_frame_years.svg",
        "assets/figures/fig2_pilot_flow.svg",
        "assets/figures/fig3_pilot_scores.svg",
    ]
    missing = [name for name in required if not (docs / name).is_file()]
    assert not missing, f"Missing site files: {missing}"


def test_required_sections_and_nav_targets(site):
    html, parser = site
    section_ids = [
        "overview",
        "questions",
        "background",
        "method",
        "results",
        "reliability",
        "reproduce",
        "references",
        "cite",
    ]
    for section_id in section_ids:
        assert section_id in parser.ids
        assert f'id="{section_id}"' in html

    nav_links = [
        values["href"]
        for tag, values in parser.tags
        if tag == "a" and "nav-link" in values.get("class", "")
    ]
    assert nav_links == [f"#{section_id}" for section_id in section_ids]
    for href in nav_links:
        assert href[1:] in parser.ids

    headings = [values for tag, values in parser.tags if tag == "h2" and "id" in values]
    assert {values["id"] for values in headings} == {
        "overview-title",
        "questions-title",
        "background-title",
        "method-title",
        "results-title",
        "reliability-title",
        "reproduce-title",
        "references-title",
        "cite-title",
    }
    for tag, values in parser.tags:
        if tag in {"section", "main", "nav"}:
            if tag == "section":
                assert values.get("aria-labelledby") in parser.ids


def test_pilot_status_is_stated_plainly(site):
    _, parser = site
    text = parser.text
    assert "Pilot draft" in text
    assert "Not peer reviewed" in text
    assert "This is a pilot, not a prevalence estimate." in text
    assert "The agreement statistics are LLM–LLM" in text
    assert "not human reliability" in text
    assert "The 900-paper full study is specified but" in text
    assert "not executed" in text
    assert "No DOI or registration record exists." in text
    assert "not submission-ready" not in text
    assert "peer-reviewed publication" not in text.lower()


def test_key_numbers_trace_to_manuscript(site):
    _, parser = site
    text = parser.text
    for number in (
        "2,666",
        "2,572",
        "136",
        "2,684",
        "2,708",
        "135",
        "2,531",
        "1/6",
        "16.7%",
        "3.0–56.4",
        "1/8",
        "12.5%",
        "2.2–47.1",
        "0.78",
        "0.86",
        "548",
    ):
        assert number in text, f"Missing pilot number: {number}"

    assert "3 of 6 primary-pair papers" in text
    assert "4 of 8 all-pair papers" in text
    assert "None of the three SWE-bench+ cases adopted the 548-instance dataset" in text
    assert "29-paper" in text or "29 selected" in text
    assert "27 full texts" in text
    assert "12 papers were coded" in text
    assert "8 were eligible" in text
    assert "6 for the two primary pairs" in text


def test_figures_are_byte_identical_copies(root: Path):
    source = root / "manuscript" / "figures"
    deployed = root / DOCS / "assets" / "figures"
    names = ["fig1_frame_years.svg", "fig2_pilot_flow.svg", "fig3_pilot_scores.svg"]
    for name in names:
        original = hashlib.sha256((source / name).read_bytes()).hexdigest()
        copy = hashlib.sha256((deployed / name).read_bytes()).hexdigest()
        assert original == copy, f"{name} was modified after copying"


def test_local_links_and_assets_resolve(root: Path, site):
    html, parser = site
    docs = (root / DOCS).resolve()
    attributes = [
        (tag, key, value)
        for tag, values in parser.tags
        for key, value in values.items()
        if key in {"href", "src"} and value
    ]
    assert attributes

    for tag, key, url in attributes:
        parts = urlsplit(url)
        if parts.scheme in {"http", "https", "mailto"}:
            continue
        if url.startswith("#"):
            assert url[1:] in parser.ids, f"Broken fragment: {url}"
            continue
        assert not parts.scheme, f"Unexpected URL scheme in {tag}[{key}]: {url}"

        target = (docs / unquote(parts.path)).resolve()
        if target.is_dir():
            target = target / "index.html"
        assert target.is_file(), f"Missing local target for {tag}[{key}]: {url}"
        assert target.is_relative_to(docs)


def test_seo_and_social_metadata(site):
    html, parser = site
    assert parser.attr("html", "lang") == ["en"]
    descriptions = [
        values["content"]
        for tag, values in parser.tags
        if tag == "meta" and values.get("name") == "description"
    ]
    assert len(descriptions) == 1 and len(descriptions[0]) >= 80
    assert parser.attr("link", "rel").count("canonical") == 1
    canonical = [
        values["href"]
        for tag, values in parser.tags
        if tag == "link" and values.get("rel") == "canonical"
    ]
    assert canonical == [CANONICAL]

    og = {
        values.get("property"): values.get("content")
        for tag, values in parser.tags
        if tag == "meta" and values.get("property", "").startswith("og:")
    }
    assert og["og:type"] == "article"
    assert og["og:url"] == CANONICAL
    assert og["og:image"] == CANONICAL + "assets/social-card.png"
    assert og["og:image:width"] == "1200"
    assert og["og:image:height"] == "630"

    twitter = {
        values.get("name"): values.get("content")
        for tag, values in parser.tags
        if tag == "meta" and values.get("name", "").startswith("twitter:")
    }
    assert twitter["twitter:card"] == "summary_large_image"
    assert twitter["twitter:image"] == CANONICAL + "assets/social-card.png"

    ld_json = [
        body
        for script_type, body in parser.inline_scripts
        if script_type == "application/ld+json"
    ]
    assert len(ld_json) == 1
    import json

    record = json.loads(ld_json[0])
    assert record["@type"] == "ScholarlyArticle"
    assert record["author"]["name"] == "Syed Abdul Aman"
    assert record["url"] == CANONICAL
    assert record["codeRepository"] == REPO
    assert "not peer reviewed" in record["creativeWorkStatus"]
    assert "not a prevalence estimate" in record["creativeWorkStatus"]
    assert "Pilot" in record["creativeWorkStatus"]


def test_citation_metadata_matches_downloadable_bibtex(root: Path, site):
    html, parser = site
    bib = (root / DOCS / "cite.bib").read_text(encoding="utf-8")
    assert "@misc{aman2026benchmarkcritique," in bib
    assert "Aman, Syed Abdul" in bib
    assert "year         = {2026}" in bib
    assert "Pilot-based research draft; not peer reviewed" in bib
    assert CANONICAL in bib
    assert REPO in bib

    assert "@misc{aman2026benchmarkcritique," in parser.text
    assert CANONICAL in parser.text
    assert "cite.bib" in html

    citation = "Aman, S. A. (2026)."
    assert citation in parser.text
    assert "[Pilot-based research draft]" in parser.text


def test_no_placeholders_or_template_copy(site):
    html, parser = site
    lower = html.lower()
    for marker in ("todo", "lorem ipsum", "part2", "[author name", "example.com", "xxx"):
        assert marker not in lower, f"Unfinished marker found: {marker}"

    assert "Benchmark Critique Diffusion" in parser.text
    assert "Does Benchmark Critique Diffuse into Evaluation Practice?" in parser.text


def test_accessibility_structure(site):
    _, parser = site
    assert parser.attr("a", "class").count("skip-link") == 1
    skip = [
        values
        for tag, values in parser.tags
        if tag == "a" and values.get("class") == "skip-link"
    ]
    assert skip[0]["href"] == "#main"
    assert "main" in parser.ids

    h1_count = sum(1 for tag, _ in parser.tags if tag == "h1")
    assert h1_count == 1

    images = [values for tag, values in parser.tags if tag == "img"]
    assert len(images) == 3
    for image in images:
        assert image.get("alt") and len(image["alt"]) > 30
        assert image.get("width") and image.get("height")
        assert image["src"].startswith("assets/figures/")

    table_regions = [
        values
        for tag, values in parser.tags
        if tag == "div" and "table-wrap" in values.get("class", "")
    ]
    tables = [values for tag, values in parser.tags if tag == "table"]
    assert len(table_regions) == len(tables) == 10
    for region in table_regions:
        assert region.get("role") == "region"
        assert region.get("tabindex") == "0"
        assert region.get("aria-labelledby") in parser.ids

    for tag, values in parser.tags:
        if tag == "th":
            assert values.get("scope") in {"col", "row"}

    buttons = [values for tag, values in parser.tags if tag == "button"]
    assert len(buttons) == 2
    assert all(button.get("type") == "button" for button in buttons)

    ledger = [
        values
        for tag, values in parser.tags
        if tag == "div" and "ledger" in values.get("class", "").split()
    ]
    assert len(ledger) == 1
    assert ledger[0].get("role") == "group"
    assert ledger[0].get("aria-label")

    wordmark = [
        values
        for tag, values in parser.tags
        if tag == "a" and "wordmark" in values.get("class", "").split()
    ]
    assert len(wordmark) == 1
    assert wordmark[0]["aria-label"].startswith("BC ")

    status_regions = [
        values
        for tag, values in parser.tags
        if tag == "span" and values.get("data-copy-status") == ""
    ]
    assert len(status_regions) == 2
    assert all(values.get("role") == "status" for values in status_regions)


def test_wide_tables_offer_a_scroll_hint(site):
    html, parser = site
    hints = [
        values
        for tag, values in parser.tags
        if tag == "span" and "scroll-hint" in values.get("class", "")
    ]
    assert len(hints) == 6
    assert html.count('class="table-wrap table--wide"') == 5
    assert html.count('class="table-wrap table--cases"') == 1
    assert "Scroll sideways for all columns." in parser.text


def test_site_is_dependency_light_and_self_hosted(site):
    html, parser = site
    assert parser.script_srcs == ["site.js"]
    for script_type, _ in parser.inline_scripts:
        assert script_type == "application/ld+json"

    assert "fonts.googleapis.com" not in html
    assert "fonts.gstatic.com" not in html
    assert "cdn." not in html
    assert "google-analytics" not in html
    assert "googletagmanager" not in html

    css = (Path(__file__).resolve().parents[1] / DOCS / "styles.css").read_text(encoding="utf-8")
    assert '@font-face' in css
    assert 'url("assets/fonts/newsreader-latin.woff2")' in css
    assert "fonts.googleapis" not in css
    assert "scroll-behavior: smooth" not in css
    assert "prefers-reduced-motion: reduce" in css
    assert "@media print" in css

    js = (Path(__file__).resolve().parents[1] / DOCS / "site.js").read_text(encoding="utf-8")
    assert "aria-current" in js
    assert "navigator.clipboard" in js
    assert "prefers-reduced-motion: reduce" in js
    assert "https://" not in js


def test_social_card_is_the_announced_size(root: Path):
    image = (root / DOCS / "assets" / "social-card.png").read_bytes()
    assert image[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", image[16:24])
    assert (width, height) == (1200, 630)
    assert len(image) > 10_000


def test_sitemap_and_robots_point_to_the_live_url(root: Path):
    docs = root / DOCS
    sitemap = ET.fromstring((docs / "sitemap.xml").read_text(encoding="utf-8"))
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [node.text for node in sitemap.findall("sm:url/sm:loc", namespace)]
    assert locations == [CANONICAL]

    robots = (docs / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *" in robots
    assert "Allow: /" in robots
    assert CANONICAL + "sitemap.xml" in robots


def test_custom_404_page_is_self_contained(root: Path):
    page = (root / DOCS / "404.html").read_text(encoding="utf-8")
    assert 'name="robots" content="noindex"' in page
    assert "/benchmark-critique-diffusion-protocol/" in page
    assert REPO in page
    assert "<script" not in page
    assert "http" in page
