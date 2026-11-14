#!/usr/bin/env python3
"""Fetch citation records for a paper from the Semantic Scholar Graph API.

This script reproduces the retrieval step that produced the frozen 2026-11-13
citation frame. It is intentionally conservative:

* It never overwrites an existing output directory unless --force is given.
* It retries HTTP 429/5xx with exponential backoff and honours Retry-After.
* It records the endpoint, retrieval timestamp, reported total, returned row
  count, and SHA-256 of the saved payload.

The frozen frame used by the study is `data/citation_frame_2666.csv`. Running
this script today creates a *new snapshot*; Semantic Scholar is live, so counts
will drift. Do not replace the frozen frame with a refresh without a registered
protocol amendment.

Usage
-----
    python scripts/fetch_citations.py \
        --paper evalplus=arXiv:2305.01210 \
        --paper swebenchplus=arXiv:2410.06992 \
        --out data/raw_refresh

Environment
-----------
S2_API_KEY   optional; raises rate limits. Never commit the key.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

S2_BASE = "https://api.semanticscholar.org/graph/v1"
DEFAULT_FIELDS = (
    "title,year,venue,publicationDate,externalIds,citationCount,authors"
)


def _request_json(url: str, *, timeout: int = 60, max_retries: int = 6) -> dict[str, Any]:
    """GET a JSON document with retry/backoff for 429 and transient 5xx."""
    headers = {
        "User-Agent": "benchmark-critique-diffusion/1.0 (research; contact: local)",
        "Accept": "application/json",
    }
    api_key = os.environ.get("S2_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key

    delay = 2.0
    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return json.loads(raw.decode("utf-8"))
        except HTTPError as exc:
            last_error = exc
            if exc.code == 429 or 500 <= exc.code < 600:
                retry_after = exc.headers.get("Retry-After")
                wait = float(retry_after) if retry_after and retry_after.isdigit() else delay
                print(
                    f"  HTTP {exc.code}; retrying in {wait:.1f}s "
                    f"(attempt {attempt}/{max_retries})",
                    file=sys.stderr,
                )
                time.sleep(wait)
                delay = min(delay * 2, 60.0)
                continue
            raise
        except (URLError, TimeoutError) as exc:
            last_error = exc
            print(
                f"  network error: {exc}; retrying in {delay:.1f}s "
                f"(attempt {attempt}/{max_retries})",
                file=sys.stderr,
            )
            time.sleep(delay)
            delay = min(delay * 2, 60.0)

    raise RuntimeError(f"Failed after {max_retries} attempts: {url}") from last_error


def fetch_citations(
    paper_id: str,
    *,
    fields: str = DEFAULT_FIELDS,
    page_size: int = 1000,
    max_records: int | None = None,
    delay: float = 1.0,
) -> tuple[list[dict[str, Any]], int | None]:
    """Return (citation rows, reported total) for one paper."""
    rows: list[dict[str, Any]] = []
    reported_total: int | None = None
    offset = 0

    while True:
        url = (
            f"{S2_BASE}/paper/{quote(paper_id, safe=':')}/citations"
            f"?fields={quote(fields, safe=',')}&limit={page_size}&offset={offset}"
        )
        payload = _request_json(url)
        if reported_total is None:
            reported_total = payload.get("total")

        batch = payload.get("data") or []
        rows.extend(batch)

        if max_records is not None and len(rows) >= max_records:
            rows = rows[:max_records]
            break
        if len(batch) < page_size:
            break
        offset += page_size
        time.sleep(delay)

    return rows, reported_total


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paper",
        action="append",
        required=True,
        metavar="KEY=S2_ID",
        help="Repeatable. Example: evalplus=arXiv:2305.01210",
    )
    parser.add_argument("--out", required=True, help="Output directory for raw JSON.")
    parser.add_argument("--fields", default=DEFAULT_FIELDS)
    parser.add_argument("--page-size", type=int, default=1000)
    parser.add_argument("--max-records", type=int, default=None)
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between pages.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    papers: list[tuple[str, str]] = []
    for spec in args.paper:
        if "=" not in spec:
            parser.error(f"--paper must be KEY=S2_ID, got: {spec}")
        key, paper_id = spec.split("=", 1)
        papers.append((key.strip(), paper_id.strip()))

    manifest: dict[str, Any] = {
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": S2_BASE,
        "fields": args.fields,
        "papers": {},
    }

    for key, paper_id in papers:
        target = out_dir / f"citations_{key}.json"
        if target.exists() and not args.force:
            print(f"Refusing to overwrite {target} (use --force).", file=sys.stderr)
            return 2

        print(f"Fetching citations for {key} ({paper_id}) ...", file=sys.stderr)
        rows, reported_total = fetch_citations(
            paper_id,
            fields=args.fields,
            page_size=args.page_size,
            max_records=args.max_records,
            delay=args.delay,
        )
        payload = {
            "key": key,
            "paper_id": paper_id,
            "retrieved_utc": datetime.now(timezone.utc).isoformat(),
            "reported_total": reported_total,
            "returned_rows": len(rows),
            "data": rows,
        }
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        target.write_bytes(encoded)
        manifest["papers"][key] = {
            "paper_id": paper_id,
            "file": target.name,
            "reported_total": reported_total,
            "returned_rows": len(rows),
            "sha256": sha256_bytes(encoded),
        }
        print(f"  saved {len(rows)} rows -> {target}", file=sys.stderr)

    manifest_path = out_dir / "retrieval_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Manifest: {manifest_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
