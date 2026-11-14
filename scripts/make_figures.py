#!/usr/bin/env python3
"""Generate dependency-free SVG figures and their source data.

matplotlib is deliberately not required. The figures are editable SVG documents
generated from the frozen pilot results and frame profile. All three figures
share one typographic and colour system so that the manuscript reads as a single
designed artifact.

Outputs
-------
manuscript/figures/fig1_frame_years.svg
manuscript/figures/fig2_pilot_flow.svg
manuscript/figures/fig3_pilot_scores.svg
manuscript/figures/fig1_frame_years.csv
manuscript/figures/fig2_pilot_flow.csv
manuscript/figures/fig3_pilot_scores.csv

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

# --- Design tokens -----------------------------------------------------------

FONT = "Segoe UI, Helvetica Neue, Arial, sans-serif"
INK = "#102a43"
INK_SOFT = "#334e68"
MUTED = "#627d98"
RULE = "#d9e2ec"
PANEL = "#f7fafc"
TEAL = "#0f766e"
TEAL_PALE = "#e6f4f1"
AMBER = "#b7791f"
AMBER_PALE = "#fdf4e3"
SLATE = "#64748b"
SLATE_PALE = "#cbd5e1"

SCORE_COLORS = {0: SLATE, 1: AMBER, 2: "#2c7a7b", 3: "#0f3d4f"}


def txt(
    x: float,
    y: float,
    content: object,
    *,
    size: float = 12,
    fill: str = INK,
    weight: int | str = 400,
    anchor: str = "start",
    spacing: float | None = None,
) -> str:
    """Return one SVG text element with the shared font stack."""
    letter_spacing = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{letter_spacing}>'
        f"{escape(str(content))}</text>"
    )


def figure_header(
    width: int,
    height: int,
    fig_id: str,
    title: str,
    desc: str,
    kicker: str,
    heading: str,
    subtitle: str,
    panel: tuple[str, str] | None = None,
) -> list[str]:
    """Return the opening SVG, accessible metadata, and shared masthead."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="{fig_id}-title {fig_id}-desc">',
        f'<title id="{fig_id}-title">{escape(title)}</title>',
        f'<desc id="{fig_id}-desc">{escape(desc)}</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<rect x="0" y="0" width="{width}" height="4" fill="{TEAL}"/>',
        txt(56, 38, kicker, size=9.5, fill=TEAL, weight=700, spacing=1.8),
        txt(56, 69, heading, size=22, fill=INK, weight=700),
        txt(56, 92, subtitle, size=12, fill=MUTED),
        f'<line x1="56" y1="112" x2="{width - 56}" y2="112" stroke="{RULE}" stroke-width="1"/>',
    ]
    if panel is not None:
        value, label = panel
        px = width - 56 - 134
        parts.extend(
            [
                f'<rect x="{px}" y="22" width="134" height="62" rx="8" fill="{PANEL}" stroke="{RULE}" stroke-width="1"/>',
                txt(px + 67, 50, value, size=20, fill=INK, weight=700, anchor="middle"),
                txt(px + 67, 68, label, size=8.5, fill=MUTED, weight=600, anchor="middle", spacing=1.2),
            ]
        )
    return parts


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


# --- Figure 1: frozen citation frame by year ---------------------------------


def frame_year_figure() -> None:
    with FRAME.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    counts = Counter(row["year"] or "unknown" for row in rows)
    order = ["2022", "2023", "2024", "2025", "2026", "unknown"]
    data = [{"year": year, "n": counts.get(year, 0)} for year in order]
    write_csv(OUT / "fig1_frame_years.csv", data, ["year", "n"])

    width, height = 900, 420
    parts = figure_header(
        width,
        height,
        "fig1",
        "Frozen citation frame by publication year",
        "Bar chart of 2,666 title clusters: 2022, 2; 2023, 119; 2024, 526; 2025, 838; 2026, 1,139; unknown, 42.",
        "FIGURE 1  /  CITATION FRAME",
        "The frozen citation frame",
        "2,666 title-level citing works, by publication year",
        panel=("2,666", "TITLE CLUSTERS"),
    )

    left, right, top, bottom = 76, 30, 152, 352
    plot_w, plot_h = width - left - right, bottom - top
    max_n = 1200
    bar_w = 78
    gap = (plot_w - bar_w * len(data)) / (len(data) - 1)

    for tick in range(0, max_n + 1, 300):
        y = bottom - (tick / max_n) * plot_h
        parts.append(f'<line x1="{left}" y1="{y}" x2="{left + plot_w}" y2="{y}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(txt(left - 12, y + 4, f"{tick:,}", size=10.5, fill=MUTED, anchor="end"))

    for index, row in enumerate(data):
        n = int(row["n"])
        bar_h = (n / max_n) * plot_h
        x = left + index * (bar_w + gap)
        y = bottom - bar_h
        if row["year"] == "2026":
            fill = AMBER
        elif row["year"] == "unknown":
            fill = SLATE_PALE
        else:
            fill = TEAL
        parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="5" fill="{fill}"/>')
        label_fill = INK_SOFT if row["year"] == "unknown" else INK
        parts.append(txt(x + bar_w / 2, y - 10, f"{n:,}", size=12.5, fill=label_fill, weight=700, anchor="middle"))
        year_label = "2026*" if row["year"] == "2026" else ("Unknown" if row["year"] == "unknown" else row["year"])
        parts.append(txt(x + bar_w / 2, bottom + 22, year_label, size=11.5, fill=INK_SOFT, weight=600, anchor="middle"))

    parts.append(f'<line x1="{left}" y1="{bottom}" x2="{left + plot_w}" y2="{bottom}" stroke="{INK_SOFT}" stroke-width="1.2"/>')
    parts.append(
        txt(
            56,
            388,
            "* 2026 is incomplete and includes 231 future-dated records. 42 clusters have no publication year.",
            size=9.5,
            fill=MUTED,
        )
    )
    parts.append(txt(56, 404, "Source: manuscript/figures/fig1_frame_years.csv.", size=9.5, fill=MUTED))
    parts.append("</svg>")
    (OUT / "fig1_frame_years.svg").write_text("\n".join(parts), encoding="utf-8", newline="\n")


# --- Figure 2: pilot flow ----------------------------------------------------


def flow_figure(results: dict) -> None:
    flow = results["flow"]
    stages = [
        ("Purposive access frame", "Purposive access frame", flow["purposive_frame"], "selected for coverage"),
        ("Full text accessible", "Full text accessible", flow["full_text_accessible"], "93.1% of the frame"),
        ("Coded with rubric", "Coded with rubric v1.0", flow["coded"], "rubric v1.0; 4 ineligible"),
        ("Eligible, all pairs", "Eligible, all pairs", flow["eligible_all_pairs"], "+2 GSM1k rows"),
        ("Eligible, primary pairs", "Eligible, primary pairs", flow["eligible_primary_pairs"], "6 of the 8 all-pair papers"),
    ]
    rows = [{"stage": csv_stage, "n": n} for _, csv_stage, n, _ in stages]
    write_csv(OUT / "fig2_pilot_flow.csv", rows, ["stage", "n"])

    width, height = 1160, 360
    parts = figure_header(
        width,
        height,
        "fig2",
        "Pilot flow from 29 purposively selected papers to 6 primary-pair eligible papers",
        "Flow diagram: 29 papers in the purposive frame, 27 accessible, 12 coded, 8 eligible for all pairs, and 6 eligible for the two primary pairs.",
        "FIGURE 2  /  PILOT FLOW",
        "From access to analysis",
        "A purposive 29-paper pilot, narrowing to six primary-pair papers",
        panel=("93.1%", "ACCESS RATE"),
    )

    start_x, box_w, box_h, gap, y = 36, 194, 104, 30, 156
    for index, (stage, _, n, note) in enumerate(stages):
        x = start_x + index * (box_w + gap)
        final = index == len(stages) - 1
        fill = TEAL_PALE if final else PANEL
        stroke = TEAL if final else RULE
        parts.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="{1.6 if final else 1}"/>')
        parts.append(txt(x + 16, y + 23, f"STEP {index + 1:02d}", size=8.5, fill=TEAL if final else MUTED, weight=700, spacing=1.3))
        parts.append(txt(x + box_w / 2, y + 66, n, size=34, fill=TEAL if final else INK, weight=700, anchor="middle"))
        parts.append(txt(x + box_w / 2, y + 88, stage, size=11.5, fill=INK_SOFT, weight=600, anchor="middle"))
        parts.append(txt(x + box_w / 2, y + box_h + 17, note, size=9.5, fill=MUTED, anchor="middle"))
        if index < len(stages) - 1:
            line_start = x + box_w + 7
            line_end = x + box_w + gap - 9
            parts.append(f'<line x1="{line_start}" y1="{y + box_h / 2}" x2="{line_end}" y2="{y + box_h / 2}" stroke="{MUTED}" stroke-width="1.5"/>')
            parts.append(
                f'<polygon points="{line_end},{y + box_h / 2} {line_end - 6},{y + box_h / 2 - 4.5} '
                f'{line_end - 6},{y + box_h / 2 + 4.5}" fill="{MUTED}"/>'
            )

    parts.append(
        txt(
            56,
            322,
            "Purposive pilot, not a probability sample. The 93.1% access rate applies only to this 29-paper frame.",
            size=9.5,
            fill=MUTED,
        )
    )
    parts.append(txt(56, 338, "Source: pilot/pilot_summary.md and analysis/pilot_results.json.", size=9.5, fill=MUTED))
    parts.append("</svg>")
    (OUT / "fig2_pilot_flow.svg").write_text("\n".join(parts), encoding="utf-8", newline="\n")


# --- Figure 3: adoption-score distribution -----------------------------------


def score_figure(results: dict) -> None:
    primary = results["primary_pair"]["score_distribution"]
    all_pair = results["all_pair"]["score_distribution"]
    labels = {0: "Citation only", 1: "Acknowledged", 2: "Partial adoption", 3: "Full adoption"}
    csv_labels = {0: "Citation only", 1: "Acknowledged", 2: "Partial", 3: "Full"}
    groups = [("Primary pairs", "n = 6", primary), ("All pairs", "n = 8  ·  includes two GSM1k rows", all_pair)]
    rows = []
    for name, _, dist in groups:
        total = sum(dist.values())
        label_name = "Primary pairs (n=6)" if name == "Primary pairs" else "All pairs (n=8)"
        for score in range(4):
            rows.append(
                {
                    "group": label_name,
                    "score": score,
                    "label": csv_labels[score],
                    "n": dist[str(score)],
                    "share": f"{dist[str(score)] / total:.4f}",
                }
            )
    write_csv(OUT / "fig3_pilot_scores.csv", rows, ["group", "score", "label", "n", "share"])

    width, height = 900, 440
    parts = figure_header(
        width,
        height,
        "fig3",
        "Pilot adoption-score distribution for primary pairs and all pairs",
        "Stacked bars: primary-pair papers have one full, three acknowledged, two citation-only, and no partial adopters. All-pair papers add one acknowledged and one citation-only GSM1k case.",
        "FIGURE 3  /  ADOPTION SCORES",
        "Adoption is not a binary",
        "Documented engagement with the critique, scored from 0 to 3",
        panel=("1/6", "FULL ADOPTION"),
    )

    bar_left, bar_width = 238, 534
    bar_height, row_gap, chart_top = 54, 36, 164
    axis_y = chart_top + 162
    for tick in (0, 25, 50, 75, 100):
        x = bar_left + (tick / 100) * bar_width
        parts.append(f'<line x1="{x}" y1="{axis_y - 6}" x2="{x}" y2="{axis_y}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(txt(x, axis_y + 14, f"{tick}%", size=9.5, fill=MUTED, anchor="middle"))

    for row_index, (name, note, dist) in enumerate(groups):
        y = chart_top + row_index * (bar_height + row_gap)
        parts.append(txt(56, y + 23, name, size=13, fill=INK, weight=700))
        parts.append(txt(56, y + 42, note, size=10, fill=MUTED))
        total = sum(dist.values())
        x_cursor = bar_left
        for score in range(4):
            n = dist[str(score)]
            if not n:
                continue
            segment_w = (n / total) * bar_width
            parts.append(
                f'<rect x="{x_cursor}" y="{y}" width="{segment_w}" height="{bar_height}" '
                f'fill="{SCORE_COLORS[score]}" stroke="#ffffff" stroke-width="2"/>'
            )
            center = x_cursor + segment_w / 2
            parts.append(txt(center, y + 26, n, size=15, fill="#ffffff", weight=700, anchor="middle"))
            parts.append(txt(center, y + 42, f"{n / total * 100:.1f}%", size=9.5, fill="#ffffff", anchor="middle"))
            x_cursor += segment_w

    legend_y = 374
    legend = [(56, 0), (232, 1), (422, 2), (612, 3)]
    for x, score in legend:
        parts.append(f'<rect x="{x}" y="{legend_y - 10}" width="11" height="11" rx="2" fill="{SCORE_COLORS[score]}"/>')
        parts.append(txt(x + 18, legend_y, f"{score}  {labels[score]}", size=10.5, fill=INK_SOFT))

    parts.append(
        txt(
            56,
            408,
            "Full adoption: 1/6 (16.7%; Wilson 95% CI 3.0–56.4%) primary; 1/8 (12.5%; 2.2–47.1%) all pairs.",
            size=9.5,
            fill=MUTED,
        )
    )
    parts.append(
        txt(
            56,
            424,
            "Bars are descriptive, not prevalence estimates. Source: manuscript/figures/fig3_pilot_scores.csv.",
            size=9.5,
            fill=MUTED,
        )
    )
    parts.append("</svg>")
    (OUT / "fig3_pilot_scores.svg").write_text("\n".join(parts), encoding="utf-8", newline="\n")


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
