# Frame Construction

## Inputs

- EvalPlus citation rows: 2,572
- SWE-bench+ citation rows: 136
- Raw sum: 2,708
- Semantic Scholar's reported EvalPlus citation count: 2,573 (one row not returned)

## Step 1: identifier union-find

Records are merged when they share any of:

- lowercased DOI,
- arXiv identifier,
- DBLP key,
- Semantic Scholar CorpusId,
- Semantic Scholar paperId.

Merging is transitive. The result is 2,684 identifier-deduplicated records. This
is an intermediate count, **not** the analysis frame.

## Step 2: title clustering

Titles are normalized by lowercasing, replacing non-alphanumeric characters with
spaces, and collapsing whitespace. Records with identical normalized titles form
one cluster. The representative record is chosen by:

1. has a DOI,
2. else has an arXiv ID,
3. else earliest publication year,
4. else lexicographically smallest paperId.

Source labels are unioned across the cluster, so a cluster can cite EvalPlus only,
SWE-bench+ only, or both.

Result: 2,666 title clusters. The 18-row reduction from 2,684 comes from 14
multi-variant clusters.

## Step 3: strata

| Stratum | Rule | N |
|---|---|---:|
| `SWE_bench_plus_census` | Any cluster citing SWE-bench+, including 23 that also cite EvalPlus | 135 |
| `EvalPlus_only_sample` | Clusters citing EvalPlus but not SWE-bench+ | 2,531 |
| **Total** | | **2,666** |

The 23 both-critique clusters are assigned to the SWE-bench+ stratum so that the
small stratum is a complete census rather than a sample.

## Step 4: freeze and hash

The source JSON SHA-256 is
`46a58fe017577d9e15c22e6bef198fdff526b511ff7897519b6a0e91542cdd72`.
The analysis CSV SHA-256 is
`6a0a374ba6120b244418e887a76a83d6bfb8a95dd61cfc822cf349ac7043d30c`.

Any post-freeze citation refresh may be reported as a sensitivity analysis but
cannot change the frame, the strata, or the denominators.

## Reference implementation

`scripts/fetch_citations.py` retrieves citation records. `scripts/build_frame.py`
performs identifier deduplication, title clustering, representative selection, and
stratum assignment. Network access is required only for retrieval; frame building
is offline and deterministic given the source JSON.
