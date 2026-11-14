#!/usr/bin/env python3
"""Build the citation analysis frame from Semantic Scholar citation records.

Pipeline
--------
1. Read raw citation payloads (``citations_*.json``) produced by
   ``fetch_citations.py``, or a pre-deduplicated ``citation_frame.json``.
2. Union records that share DOI / arXiv / DBLP / CorpusId / Semantic Scholar
   paperId.  This yields the *identifier-deduplicated* intermediate.
3. Cluster the deduplicated records by normalised title.  This yields the
   *analysis frame* used for sampling.
4. Assign strata:
   - ``SWE_bench_plus_census``: cites SWE-bench+ (with or without EvalPlus)
   - ``EvalPlus_only_sample``: cites EvalPlus only
5. Write CSV + JSON/Markdown summaries with SHA-256 checksums.

The frozen frame is ``data/citation_frame_2666.csv`` (2,666 clusters). This
script is a reproducible rebuild; because Semantic Scholar is live, a fresh
retrieval will not reproduce the frozen hashes exactly. Never overwrite the
frozen frame from a refresh without a protocol amendment.

Usage
-----
    python scripts/build_frame.py --raw-dir data/raw_refresh --out data/rebuilt
    python scripts/build_frame.py --frame-json citation_frame.json --out data/rebuilt
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

CSV_FIELDS = [
    "cluster_id",
    "stratum",
    "title",
    "year",
    "publicationDate",
    "venue",
    "doi",
    "arxiv",
    "dblp",
    "corpusId",
    "paperId",
    "cites",
    "n_title_variants",
]


def norm_title(title: str | None) -> str:
    """Lowercase, replace non-alphanumerics with spaces, collapse whitespace."""
    text = (title or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def identifier_keys(record: dict[str, Any]) -> list[str]:
    keys: list[str] = []
    if record.get("doi"):
        keys.append("doi:" + str(record["doi"]).strip().lower())
    if record.get("arxiv"):
        keys.append("arxiv:" + str(record["arxiv"]).strip().lower())
    if record.get("dblp"):
        keys.append("dblp:" + str(record["dblp"]).strip().lower())
    if record.get("corpusId"):
        keys.append("corpus:" + str(record["corpusId"]))
    if record.get("paperId"):
        keys.append("s2:" + str(record["paperId"]))
    return keys


class DisjointSet:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def add(self, item: str) -> None:
        self.parent.setdefault(item, item)

    def find(self, item: str) -> str:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            nxt = self.parent[item]
            self.parent[item] = root
            item = nxt
        return root

    def union(self, left: str, right: str) -> None:
        root_left, root_right = self.find(left), self.find(right)
        if root_left != root_right:
            self.parent[root_right] = root_left


def load_raw_citations(raw_dir: Path) -> list[tuple[str, dict[str, Any]]]:
    """Return [(source_key, payload)] from citations_*.json files."""
    payloads: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(raw_dir.glob("citations_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        key = payload.get("key") or path.stem.removeprefix("citations_")
        payloads.append((key, payload))
    if not payloads:
        raise SystemExit(f"No citations_*.json files found in {raw_dir}")
    return payloads


def rows_from_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Accept both the study's {'meta','rows'} shape and S2's {'data'} shape."""
    if isinstance(payload.get("rows"), list):
        return payload["rows"]
    if isinstance(payload.get("data"), list):
        rows = []
        for item in payload["data"]:
            # S2 citations endpoint nests the citing paper under "citingPaper".
            rows.append(item.get("citingPaper", item))
        return rows
    raise SystemExit("Unrecognised citation payload shape")


def identifier_deduplicate(
    payloads: Iterable[tuple[str, dict[str, Any]]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    dsu = DisjointSet()
    per_source: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    raw_counts: dict[str, int] = {}
    reported_counts: dict[str, int | None] = {}

    for key, payload in payloads:
        rows = rows_from_payload(payload)
        raw_counts[key] = len(rows)
        reported_counts[key] = (payload.get("meta") or {}).get("citationCount")
        for record in rows:
            keys = identifier_keys(record)
            if not keys:
                continue
            for k in keys:
                dsu.add(k)
            for k in keys[1:]:
                dsu.union(keys[0], k)
            per_source[key].append(record)

    cluster_sources: dict[str, set[str]] = collections.defaultdict(set)
    cluster_rep: dict[str, dict[str, Any]] = {}
    for key, records in per_source.items():
        for record in records:
            keys = identifier_keys(record)
            if not keys:
                continue
            root = dsu.find(keys[0])
            cluster_sources[root].add(key)
            cluster_rep.setdefault(root, record)

    unique_counts = {
        key: len({dsu.find(identifier_keys(r)[0]) for r in records if identifier_keys(r)})
        for key, records in per_source.items()
    }
    union_roots = set(cluster_sources)
    overlaps = {
        key: {dsu.find(identifier_keys(r)[0]) for r in records if identifier_keys(r)}
        for key, records in per_source.items()
    }
    overlap = set.intersection(*overlaps.values()) if len(overlaps) > 1 else set()

    frame: list[dict[str, Any]] = []
    for root in union_roots:
        record = dict(cluster_rep[root])
        record["cites"] = sorted(cluster_sources[root])
        frame.append(record)
    frame.sort(key=lambda r: (str(r.get("year") or ""), (r.get("title") or "").lower()))

    summary = {
        "raw": raw_counts,
        "reported": reported_counts,
        "unique": {**unique_counts, "union": len(union_roots), "overlap": len(overlap)},
    }
    return frame, summary


def title_cluster(frame: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for record in frame:
        groups[norm_title(record.get("title"))].append(record)

    clusters: list[dict[str, Any]] = []
    for _key, rows in groups.items():
        cites = sorted({c for r in rows for c in r.get("cites", [])})
        def rank(record: dict[str, Any]) -> tuple[int, int, int, str]:
            return (
                0 if record.get("doi") else 1,
                0 if record.get("arxiv") else 1,
                record.get("year") or 9999,
                record.get("paperId") or "",
            )
        representative = dict(sorted(rows, key=rank)[0])
        representative["cites"] = cites
        representative["n_title_variants"] = len(rows)
        representative["stratum"] = (
            "SWE_bench_plus_census" if "swebenchplus" in cites else "EvalPlus_only_sample"
        )
        clusters.append(representative)

    clusters.sort(key=lambda r: (str(r.get("year") or "9999"), (r.get("title") or "").lower()))
    return clusters


def write_outputs(clusters: list[dict[str, Any]], out_dir: Path, source_note: str,
                  identifier_rows: int, dedup_summary: dict[str, Any]) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "citation_frame.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for index, record in enumerate(clusters, 1):
            writer.writerow({
                "cluster_id": f"C{index:04d}",
                "stratum": record["stratum"],
                "title": record.get("title") or "",
                "year": record.get("year") or "",
                "publicationDate": record.get("publicationDate") or "",
                "venue": record.get("venue") or "",
                "doi": record.get("doi") or "",
                "arxiv": record.get("arxiv") or "",
                "dblp": record.get("dblp") or "",
                "corpusId": record.get("corpusId") or "",
                "paperId": record.get("paperId") or "",
                "cites": "+".join(record["cites"]),
                "n_title_variants": record["n_title_variants"],
            })

    years = collections.Counter(str(c.get("year") or "unknown") for c in clusters)
    strata = collections.Counter(c["stratum"] for c in clusters)
    summary = {
        "generated_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "source": source_note,
        "identifier_dedup_rows": identifier_rows,
        "title_clusters": len(clusters),
        "strata": dict(strata),
        "cites_combinations": dict(collections.Counter("+".join(c["cites"]) for c in clusters)),
        "years": dict(sorted(years.items())),
        "identifier_coverage": {
            "doi": sum(1 for c in clusters if c.get("doi")),
            "arxiv": sum(1 for c in clusters if c.get("arxiv")),
            "dblp": sum(1 for c in clusters if c.get("dblp")),
            "no_doi_arxiv_dblp": sum(
                1 for c in clusters if not any(c.get(k) for k in ("doi", "arxiv", "dblp"))
            ),
        },
        "no_publication_date": sum(1 for c in clusters if not c.get("publicationDate")),
        "publication_date_after_2026_09_30": sum(
            1 for c in clusters if (c.get("publicationDate") or "") > "2026-09-30"
        ),
        "multi_variant_clusters": sum(1 for c in clusters if c["n_title_variants"] > 1),
        "identifier_dedup": dedup_summary,
        "sha256": {
            "frame_csv": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        },
    }

    (out_dir / "frame_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# Citation frame profile\n\n",
        f"Generated: {summary['generated_utc'][:10]}  \n",
        f"Source: {source_note}\n\n",
        "## Counts\n\n| Quantity | Count |\n|---|---:|\n",
        f"| Identifier-deduplicated union | {identifier_rows:,} |\n",
        f"| Title-deduplicated clusters (analysis frame) | {len(clusters):,} |\n",
        f"| SWE-bench+ stratum (census) | {strata.get('SWE_bench_plus_census', 0):,} |\n",
        f"| EvalPlus-only stratum (sample) | {strata.get('EvalPlus_only_sample', 0):,} |\n",
        f"| Both critiques | {sum(1 for c in clusters if len(c['cites']) == 2):,} |\n\n",
        "## Year distribution (title clusters)\n\n| Year | Count |\n|---|---:|\n",
    ]
    for year, count in sorted(years.items()):
        lines.append(f"| {year} | {count:,} |\n")
    lines += ["\n## Identifier coverage\n\n| Field | Count |\n|---|---:|\n"]
    for key, value in summary["identifier_coverage"].items():
        lines.append(f"| {key} | {value:,} |\n")
    lines += [
        "\n## Data quality flags\n\n",
        f"- No publication date: {summary['no_publication_date']:,}\n",
        f"- Publication date after 2026-09-30: {summary['publication_date_after_2026_09_30']:,}\n",
        f"- Clusters with >1 title variant: {summary['multi_variant_clusters']:,}\n\n",
        "## SHA-256\n\n",
        f"- `frame_csv`: `{summary['sha256']['frame_csv']}`\n",
    ]
    (out_dir / "frame_summary.md").write_text("".join(lines), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--raw-dir", type=Path, help="Directory of citations_*.json files.")
    source.add_argument("--frame-json", type=Path, help="Pre-deduplicated frame JSON.")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--force", action="store_true", help="Overwrite output files.")
    args = parser.parse_args()

    if (args.out / "citation_frame.csv").exists() and not args.force:
        print(f"Refusing to overwrite {args.out/'citation_frame.csv'} (use --force).", file=sys.stderr)
        return 2

    if args.frame_json:
        frame = json.loads(args.frame_json.read_text(encoding="utf-8"))
        if isinstance(frame, dict):
            frame = frame.get("rows") or frame.get("data") or []
        dedup_summary = {"note": "pre-deduplicated frame supplied"}
        identifier_rows = len(frame)
        source_note = f"Rebuilt from pre-deduplicated frame: {args.frame_json.name}"
    else:
        payloads = load_raw_citations(args.raw_dir)
        frame, dedup_summary = identifier_deduplicate(payloads)
        identifier_rows = len(frame)
        source_note = (
            "Semantic Scholar Graph API citations rebuilt by scripts/build_frame.py"
        )

    clusters = title_cluster(frame)
    summary = write_outputs(clusters, args.out, source_note, identifier_rows, dedup_summary)
    print(json.dumps({k: summary[k] for k in ("title_clusters", "strata", "years", "sha256")},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
