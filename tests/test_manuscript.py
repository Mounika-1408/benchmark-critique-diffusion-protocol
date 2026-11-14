from __future__ import annotations

import re
from pathlib import Path


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def test_status_banner_is_honest(paper):
    assert "PILOT-BASED RESEARCH DRAFT" in paper
    assert "NOT A COMPLETED FULL-SCALE STUDY" in paper
    assert "does **not** estimate the prevalence" in paper
    assert "submission-ready" in paper
    assert "full-scale study" in paper


def test_no_unfinished_placeholders(paper):
    assert "PART2" not in paper
    assert "TODO" not in paper
    assert "[Author name" not in paper
    assert "lorem ipsum" not in paper.lower()


def test_author_is_identified(paper):
    assert "Syed Abdul Aman" in paper
    assert "Independent Researcher" in paper or "independent researcher" in paper


def test_core_frame_numbers(paper):
    for text in ("2,666", "2,684", "2,708", "135", "2,531"):
        assert text in paper


def test_pilot_flow_numbers(paper):
    for text in ("29-paper", "27", "12 papers", "8 were eligible", "6 for the two primary pairs"):
        assert text in paper


def test_primary_results_are_present_and_consistent(paper):
    assert "1/6" in paper
    assert "16.7%" in paper
    assert "3.0" in paper and "56.4" in paper
    assert "2 citation-only, 3 acknowledged, 0 partial, and 1 full" in paper
    assert "5/6" in paper
    assert "83.3%" in paper


def test_all_pair_results_are_present_and_consistent(paper):
    assert "1/8" in paper
    assert "12.5%" in paper
    assert "2.2" in paper and "47.1" in paper
    assert "3 citation-only, 4 acknowledged, 0 partial, and 1 full" in paper


def test_reliability_is_not_reported_as_human(paper):
    assert "LLM–LLM" in paper
    assert "rather than human inter-rater reliability" in paper or "not** human inter-rater reliability" in paper
    assert "0.78" in paper and "0.86" in paper
    assert "No human second coder" in paper or "no human second coder" in paper


def test_no_preregistration_claim(paper):
    lower = paper.lower()
    assert "not** been registered" in lower or "not been registered" in lower
    assert "not preregistered" in lower
    assert "does not describe the study as preregistered" in lower
    assert "osf" in lower


def test_full_scale_is_labeled_as_plan(paper):
    assert "This design was not executed" in paper or "not executed" in paper
    assert "plan, not a result" in paper
    assert "900" in paper
    assert "1,200" in paper


def test_abstract_length_and_content(abstract):
    body = abstract.split("**Keywords:**")[0]
    body = body.replace("# Abstract", "")
    assert 150 <= word_count(body) <= 250
    for text in ("2,666", "29-paper", "1/6", "16.7%", "1/8", "12.5%", "LLM"):
        assert text in abstract
    assert "human reliability" in abstract


def test_manuscript_has_required_sections(paper):
    required = [
        "Abstract",
        "Keywords",
        "Introduction",
        "Research Questions and Hypotheses",
        "Related Work",
        "Conceptual Framework",
        "Methodology",
        "Citation-Frame Construction",
        "Sampling and Eligibility",
        "Coding Rubric and Reliability",
        "Results",
        "Statistical Analysis",
        "Discussion",
        "Threats to Validity",
        "Limitations",
        "Ethics and Licensing",
        "Reproducibility and Data Availability",
        "Conclusion",
        "References",
    ]
    headings = "\n".join(re.findall(r"^## .*$", paper, re.M))
    for section in required:
        assert section in headings


def test_key_cases_are_reported(paper):
    for key in (
        "whatswrong",
        "utboost",
        "schrodinger",
        "calibration",
        "reagent",
        "correctness_internal",
        "understand_translate",
        "promptcot",
    ):
        assert f"`{key}`" in paper


def test_references_bib_is_populated(root):
    bib = (root / "manuscript" / "references.bib").read_text(encoding="utf-8")
    entries = re.findall(r"^@\w+\{", bib, re.M)
    assert len(entries) >= 15
    for key in ("rogers2003diffusion", "small1978cited", "kapoor2023leakage"):
        assert f"{{{key}," in bib
    assert "10.1177/030631277800800305" in bib


def test_figures_and_tables_are_referenced(paper):
    for label in ("Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6"):
        assert label in paper
    for label in ("Figure 1", "Figure 2", "Figure 3"):
        assert label in paper


def test_limitations_are_explicit(paper):
    for text in (
        "purposive",
        "No human reliability",
        "full-scale study was not executed",
        "Semantic Scholar snapshot",
        "not registered",
        "Licensing constraints",
    ):
        assert text in paper
