# Milestone 4 Spec (v0.4.0)

## 1. Milestone Scope

This document specifies the final production-readiness work for the Vancouver Food Programs dashboard in Milestone 4. The scope includes performance hardening with parquet plus DuckDB query pushdown, one advanced feature implementation, behavior and unit testing, and structured resolution of instructor, TA, and peer feedback.

The M4 goal is to ship a stable, documented, and test-backed release on Posit Connect Cloud with clear team collaboration records in GitHub Issues, PRs, and release notes.

---

## 2. Our Deliverables

| Deliverable | Planned Evidence |
|---|---|
| Working app on Posit Connect Cloud | Stable URL in README/About and v0.4.0 release notes |
| Parquet + DuckDB query path | App reads from data/processed/food_programs.parquet via ibis DuckDB table |
| One advanced feature | Option D selected and already present (component click event interaction) |
| Tests | At least 3 Playwright behavior tests + 1 pytest unit test |
| Feedback prioritization issue | GitHub issue titled M4 Feedback Prioritization | Planned |
| Feedback addressed | Instructor and TA feedback items implemented; peer items documented and triaged |
| CONTRIBUTING.md update | M3 retrospective + M4 norms, merged via PR |
| Spec docs updated before code | This document and issue/design notes updated first |
| CHANGELOG 0.4.0 | Added, Changed, Fixed, Known Issues, Release Highlight, Collaboration, Reflection |
| GitHub release v0.4.0 | Release notes summarize merged PRs and reflection |
| Gradescope submission | PDF linking release |

---

