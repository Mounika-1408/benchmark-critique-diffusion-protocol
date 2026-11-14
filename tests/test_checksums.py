from __future__ import annotations

from pathlib import Path


def test_checksums_verify(root):
    import verify_checksums

    assert verify_checksums.verify(root) == 0


def test_checksum_file_has_no_duplicates(root):
    text = (root / "reproducibility" / "checksums.sha256").read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    paths = [line.split(None, 1)[1] for line in lines]
    assert len(paths) == len(set(paths))
    assert len(lines) >= 25


def test_frozen_frame_hash_is_recorded(root):
    summary = (root / "data" / "frame_summary.json").read_text(encoding="utf-8")
    assert "6a0a374ba6120b244418e887a76a83d6bfb8a95dd61cfc822cf349ac7043d30c" in summary
    assert "46a58fe017577d9e15c22e6bef198fdff526b511ff7897519b6a0e91542cdd72" in summary


def test_checksums_cover_pilot_and_frame(root):
    text = (root / "reproducibility" / "checksums.sha256").read_text(encoding="utf-8")
    assert "data/citation_frame_2666.csv" in text
    assert "pilot/pilot_coding_table.csv" in text
    assert "manuscript/paper.md" in text
