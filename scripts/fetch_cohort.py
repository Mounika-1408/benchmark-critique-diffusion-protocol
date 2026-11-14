#!/usr/bin/env python3
"""Retrieve arXiv metadata and full texts for a cohort.

This is the empirical retrieval step for the bounded cohort. It does not
bypass paywalls: only arXiv records are retrieved. Non-arXiv records are
logged as inaccessible (or as metadata-only) and are handled in the analysis
as a documented open-access restriction.

Outputs
-------
data/cohort_arxiv_metadata.csv   one row per arXiv record
data/cohort_retrieval_log.csv    one row per cohort record
<TEMP>/p2study/pdfs/*.pdf        working copies, NOT redistributed
<TEMP>/p2study/texts/*.txt       extracted text, NOT redistributed

Usage
-----
    python scripts/fetch_cohort.py \
        --cohort data/cohort_feasibility.csv \
        --workdir "$env:TEMP/p2study" \
        --delay 1.0
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"


def request_bytes(url: str, *, timeout: int = 90, retries: int = 5) -> bytes:
    headers = {"User-Agent": "benchmark-critique-diffusion/1.0 (research)"}
    delay = 2.0
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urlopen(Request(url, headers=headers), timeout=timeout) as response:
                return response.read()
        except HTTPError as exc:
            last_error = exc
            if exc.code in (429, 500, 502, 503, 504):
                wait = delay
                retry_after = exc.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    wait = max(wait, float(retry_after))
                print(f"  HTTP {exc.code}; waiting {wait:.0f}s ({attempt}/{retries})", file=sys.stderr)
                time.sleep(wait)
                delay = min(delay * 2, 60)
                continue
            raise
        except (URLError, TimeoutError) as exc:
            last_error = exc
            print(f"  network error {exc}; waiting {delay:.0f}s ({attempt}/{retries})", file=sys.stderr)
            time.sleep(delay)
            delay = min(delay * 2, 60)
    raise RuntimeError(f"Failed after {retries} attempts: {url}") from last_error


def fetch_metadata(ids: list[str], batch_size: int = 50, delay: float = 3.0) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for start in range(0, len(ids), batch_size):
        batch = ids[start:start + batch_size]
        url = f"{ARXIV_API}?id_list={','.join(batch)}&max_results={len(batch)}"
        print(f"Metadata batch {start // batch_size + 1}: {len(batch)} ids", file=sys.stderr)
        raw = request_bytes(url)
        root = ET.fromstring(raw)
        for entry in root.findall(f"{ATOM}entry"):
            entry_id = entry.findtext(f"{ATOM}id", default="")
            match = re.search(r"abs/([^v]+)(?:v\d+)?$", entry_id)
            if not match:
                continue
            key = match.group(1)
            authors = [
                author.findtext(f"{ATOM}name", default="")
                for author in entry.findall(f"{ATOM}author")
            ]
            records[key] = {
                "arxiv": key,
                "title_api": " ".join((entry.findtext(f"{ATOM}title", default="") or "").split()),
                "abstract": " ".join((entry.findtext(f"{ATOM}summary", default="") or "").split()),
                "published": entry.findtext(f"{ATOM}published", default=""),
                "updated": entry.findtext(f"{ATOM}updated", default=""),
                "journal_ref": entry.findtext(f"{ARXIV_NS}journal_ref", default=""),
                "doi_api": entry.findtext(f"{ARXIV_NS}doi", default=""),
                "primary_category": (
                    entry.find(f"{ARXIV_NS}primary_category").attrib.get("term", "")
                    if entry.find(f"{ARXIV_NS}primary_category") is not None else ""
                ),
                "authors": "; ".join(authors),
            }
        time.sleep(delay)
    return records


def download_pdf(arxiv_id: str, target: Path, delay: float = 1.0) -> tuple[bool, str]:
    if target.exists() and target.stat().st_size > 10_000:
        return True, "cached"
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    try:
        raw = request_bytes(url, timeout=120, retries=4)
        if not raw.startswith(b"%PDF"):
            return False, "not a PDF"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        time.sleep(delay)
        return True, "downloaded"
    except Exception as exc:  # noqa: BLE001 - log and continue
        return False, str(exc)[:200]


def extract_text(pdf: Path, target: Path) -> tuple[bool, str]:
    if target.exists() and target.stat().st_size > 1000:
        return True, "cached"
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["pdftotext", "-layout", str(pdf), str(target)],
            check=True, capture_output=True, timeout=120,
        )
        if target.exists() and target.stat().st_size > 1000:
            return True, "pdftotext"
    except Exception:
        pass
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        target.write_text(text, encoding="utf-8")
        return (target.stat().st_size > 1000), "pypdf"
    except Exception as exc:  # noqa: BLE001
        return False, f"extract failed: {exc}"[:200]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort", type=Path, required=True)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()

    with args.cohort.open(encoding="utf-8", newline="") as handle:
        cohort = list(csv.DictReader(handle))

    arxiv_ids = sorted({r["arxiv"].strip() for r in cohort if r.get("arxiv", "").strip()})
    print(f"Cohort: {len(cohort)} records; arXiv ids: {len(arxiv_ids)}", file=sys.stderr)

    metadata = fetch_metadata(arxiv_ids)
    data_dir = args.cohort.parent
    metadata_path = data_dir / "cohort_arxiv_metadata.csv"
    metadata_fields = [
        "arxiv", "title_api", "abstract", "published", "updated",
        "journal_ref", "doi_api", "primary_category", "authors",
    ]
    with metadata_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=metadata_fields)
        writer.writeheader()
        for arxiv_id in arxiv_ids:
            writer.writerow(metadata.get(arxiv_id, {"arxiv": arxiv_id}))

    pdf_dir = args.workdir / "pdfs"
    text_dir = args.workdir / "texts"
    log_rows: list[dict[str, Any]] = []
    for index, record in enumerate(cohort, 1):
        arxiv_id = (record.get("arxiv") or "").strip()
        status = "no_arxiv_id"
        chars = 0
        if arxiv_id:
            pdf_path = pdf_dir / f"{arxiv_id.replace('/', '_')}.pdf"
            text_path = text_dir / f"{arxiv_id.replace('/', '_')}.txt"
            ok, message = download_pdf(arxiv_id, pdf_path, delay=args.delay)
            if ok:
                extracted, extract_message = extract_text(pdf_path, text_path)
                if extracted:
                    status = "accessible"
                    chars = text_path.stat().st_size
                else:
                    status = "text_extraction_failed"
                    message = extract_message
            else:
                status = "pdf_download_failed"
                message = message
            if index % 25 == 0:
                print(f"  {index}/{len(cohort)}: {status}", file=sys.stderr)
        else:
            message = "no arXiv id; paywalled/landing page not retrieved"
        log_rows.append({
            "cluster_id": record["cluster_id"],
            "design_role": record["design_role"],
            "arxiv": arxiv_id,
            "doi": record.get("doi", ""),
            "retrieval_status": status,
            "text_chars": chars,
            "failure_reason": "" if status == "accessible" else message,
            "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        })

    log_path = data_dir / "cohort_retrieval_log.csv"
    with log_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(log_rows[0]))
        writer.writeheader()
        writer.writerows(log_rows)

    accessible = sum(1 for row in log_rows if row["retrieval_status"] == "accessible")
    print(f"Accessible: {accessible}/{len(cohort)} ({accessible/len(cohort)*100:.1f}%)", file=sys.stderr)
    print(f"Metadata: {metadata_path}", file=sys.stderr)
    print(f"Retrieval log: {log_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
