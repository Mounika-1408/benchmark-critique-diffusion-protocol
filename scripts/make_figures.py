#!/usr/bin/env python3
"""Generate dependency-free SVG figures and their source data.

matplotlib is deliberately not required. The figures are simple, editable SVG
documents generated from the frozen pilot results and frame profile.

Outputs
-------
manuscript/figures/fig2_pilot_flow.svg
manuscript/figures/fig3_pilot_scores.svg
manuscript/figures/fig1_frame_years.svg
manuscript/figures/fig2_pilot_flow.csv
manuscript/figures/fig3_pilot_scores.csv
manuscript/figures/fig1_frame_years.csv

Usage
-----
    python scripts/analyze_pilot.py
    python scripts/make_figures.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
FRAME = ROOT / "data" / "citation_frame_2666.csv"
RESULTS = ROOT / "analysis" / "pilot_results.json"
OUT = ROOT / "manuscript" / "figures"

NAVY = "#17324d"
TEAL = "#2a7f8f"
GOLD = "#c58b2a"
GREY = "#8c97a3"
LIGHT = "#edf2f6"
INK = "#1d2733"


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def flow_figure(results: dict) -> None:
    flow = results["flow"]
    stages = [
        ("Purposive access frame", flow["purposive_frame"]),
        ("Full text accessible", flow["full_text_accessible"]),
        ("Coded with rubric v1.0", flow["coded"]),
        ("Eligible, all pairs", flow["eligible_all_pairs"]),
        ("Eligible, primary pairs", flow["eligible_primary_pairs"]),
    ]
    rows = [{"stage": stage, "n": n} for stage, n in stages]
    write_csv(OUT / "fig2_pilot_flow.csv", rows, ["stage", "n"])

    width, height = 1120, 270
    box_w, box_h, gap = 190, 96, 26
    start_x, y = 28, 86
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="fig1-title fig1-desc">',
        '<title id="fig1-title">Pilot flow from 29 purposively selected papers to 6 primary-pair eligible papers</title>',
        '<desc id="fig1-desc">Flow diagram: 29 papers in the purposive frame, 27 accessible, 12 coded, 8 eligible for all pairs, and 6 eligible for the two primary pairs.</desc>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="28" y="34" font-family="Segoe UI, Arial, sans-serif" font-size="19" font-weight="700" fill="{INK}">Pilot flow: access, coding, and eligibility</text>',
        f'<text x="28" y="56" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{GREY}">Purposive pilot; not a probability sample and not a prevalence estimate.</text>',
    ]
    for index, (stage, n) in enumerate(stages):
        x = start_x + index * (box_w + gap)
        fill = LIGHT if index < 4 else "#e8f2f2"
        stroke = NAVY if index < 4 else TEAL
        parts.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x + box_w/2}" y="{y + 38}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="700" fill="{stroke}">{n}</text>')
        parts.append(f'<text x="{x + box_w/2}" y="{y + 66}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{INK}">{escape(stage)}</text>')
        if index < len(stages) - 1:
            ax = x + box_w + 5
            parts.append(f'<line x1="{ax}" y1="{y + box_h/2}" x2="{ax + gap - 10}" y2="{y + box_h/2}" stroke="{GREY}" stroke-width="2"/>')
            parts.append(f'<polygon points="{ax + gap - 10},{y + box_h/2} {ax + gap - 18},{y + box_h/2 - 5} {ax + gap - 18},{y + box_h/2 + 5}" fill="{GREY}"/>')
    parts.append(f'<text x="28" y="{height - 28}" font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="{GREY}">Source: pilot/pilot_summary.md and pilot/pilot_coding_table.csv. The 93.1% access rate applies only to this purposive frame.</text>')
    parts.append("</svg>")
    (OUT / "fig2_pilot_flow.svg").write_text("\n".join(parts), encoding="utf-8")


def score_figure(results: dict) -> None:
    primary = results["primary_pair"]["score_distribution"]
    all_pair = results["all_pair"]["score_distribution"]
    labels = {0: "Citation only", 1: "Acknowledged", 2: "Partial", 3: "Full"}
    colors = {0: GREY, 1: GOLD, 2: TEAL, 3: NAVY}
    groups = [("Primary pairs (n=6)", primary), ("All pairs (n=8)", all_pair)]
    rows = []
    for name, dist in groups:
        total = sum(dist.values())
        for score in range(4):
            rows.append({"group": name, "score": score, "label": labels[score], "n": dist[str(score)], "share": f"{dist[str(score)] / total:.4f}"})
    write_csv(OUT / "fig3_pilot_scores.csv", rows, ["group", "score", "label", "n", "share"])

    width, height = 760, 430
    left, right, top, bottom = 90, 40, 78, 82
    plot_w, plot_h = width - left - right, height - top - bottom
    bar_w, group_gap = 110, 150
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="fig2-title fig2-desc">',
        '<title id="fig2-title">Pilot adoption-score distribution for primary pairs and all pairs</title>',
        '<desc id="fig2-desc">Stacked bars: primary-pair papers have one full, three acknowledged, two citation-only, and no partial adopters. All-pair papers add one acknowledged and one citation-only GSM1k case.</desc>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="{left}" y="34" font-family="Segoe UI, Arial, sans-serif" font-size="19" font-weight="700" fill="{INK}">Pilot adoption-score distribution</text>',
        f'<text x="{left}" y="56" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{GREY}">Counts are tiny; bars are descriptive, not prevalence estimates.</text>',
    ]
    for tick in range(0, 101, 25):
        y = top + plot_h - (tick / 100) * plot_h
        parts.append(f'<line x1="{left}" y1="{y}" x2="{left + plot_w}" y2="{y}" stroke="#e1e7ed" stroke-width="1"/>')
        parts.append(f'<text x="{left - 10}" y="{y + 4}" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="{GREY}">{tick}%</text>')
    for group_index, (name, dist) in enumerate(groups):
        total = sum(dist.values())
        x = left + 90 + group_index * (bar_w + group_gap)
        y_cursor = top + plot_h
        for score in range(3, -1, -1):
            share = dist[str(score)] / total
            h = share * plot_h
            y_cursor -= h
            parts.append(f'<rect x="{x}" y="{y_cursor}" width="{bar_w}" height="{h}" fill="{colors[score]}" stroke="white" stroke-width="1.5"/>')
            if dist[str(score)]:
                parts.append(f'<text x="{x + bar_w/2}" y="{y_cursor + h/2 + 5}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700" fill="white">{dist[str(score)]}</text>')
        parts.append(f'<text x="{x + bar_w/2}" y="{top + plot_h + 24}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{INK}">{escape(name)}</text>')
    legend_x, legend_y = left + 20, height - 34
    for index, score in enumerate([0, 1, 2, 3]):
        x = legend_x + index * 158
        parts.append(f'<rect x="{x}" y="{legend_y - 11}" width="13" height="13" fill="{colors[score]}"/>')
        parts.append(f'<text x="{x + 20}" y="{legend_y}" font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="{INK}">{labels[score]}</text>')
    parts.append("</svg>")
    (OUT / "fig3_pilot_scores.svg").write_text("\n".join(parts), encoding="utf-8")


def frame_year_figure() -> None:
    with FRAME.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    counts = Counter(row["year"] or "unknown" for row in rows)
    order = ["2022", "2023", "2024", "2025", "2026", "unknown"]
    data = [{"year": year, "n": counts.get(year, 0)} for year in order]
    write_csv(OUT / "fig1_frame_years.csv", data, ["year", "n"])

    width, height = 700, 340
    left, right, top, bottom = 70, 30, 72, 58
    plot_w, plot_h = width - left - right, height - top - bottom
    max_n = max(row["n"] for row in data)
    bar_gap = 16
    bar_w = (plot_w - bar_gap * (len(data) - 1)) / len(data)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="fig3-title fig3-desc">',
        '<title id="fig3-title">Citation-frame clusters by publication year</title>',
        '<desc id="fig3-desc">Bar chart: 2 clusters from 2022, 119 from 2023, 526 from 2024, 838 from 2025, 1,139 from 2026, and 42 unknown.</desc>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="{left}" y="34" font-family="Segoe UI, Arial, sans-serif" font-size="19" font-weight="700" fill="{INK}">Frozen frame by publication year</text>',
        f'<text x="{left}" y="55" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{GREY}">2,666 title clusters; 2026 is incomplete and includes 231 future-dated records.</text>',
    ]
    for tick in range(0, max_n + 1, 250):
        y = top + plot_h - (tick / max_n) * plot_h
        parts.append(f'<line x1="{left}" y1="{y}" x2="{left + plot_w}" y2="{y}" stroke="#e1e7ed" stroke-width="1"/>')
        parts.append(f'<text x="{left - 10}" y="{y + 4}" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="{GREY}">{tick}</text>')
    for index, row in enumerate(data):
        h = (row["n"] / max_n) * plot_h
        x = left + index * (bar_w + bar_gap)
        y = top + plot_h - h
        parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="{TEAL}"/>')
        parts.append(f'<text x="{x + bar_w/2}" y="{y - 7}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="{INK}">{row["n"]:,}</text>')
        parts.append(f'<text x="{x + bar_w/2}" y="{top + plot_h + 20}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="{INK}">{row["year"]}</text>')
    parts.append("</svg>")
    (OUT / "fig1_frame_years.svg").write_text("\n".join(parts), encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    flow_figure(results)
    score_figure(results)
    frame_year_figure()
    print(f"Wrote 3 SVG figures and CSV data to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

