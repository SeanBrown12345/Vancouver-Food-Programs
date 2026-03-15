# Milestone 4 Spec (v0.4.0)

## 1. Milestone Scope

This document specifies the final production-readiness work for the Vancouver Food Programs dashboard in Milestone 4. The scope includes performance hardening with parquet plus DuckDB query pushdown, one advanced feature implementation, behavior and unit testing, and structured resolution of instructor, TA, and peer feedback.

The M4 goal is to ship a stable, documented, and test-backed release on Posit Connect Cloud with clear team collaboration records in GitHub Issues, PRs, and release notes.

---

## 2. Our M4 Deliverables

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
## 3. Existing Core Dashboard Behavior

Our app currently supports:

- Filtering by meal cost, local area, and service features.
- Map-based exploration of programs with detail and contact panels.
- AI Explorer tab for natural-language filtering



## 4. Advanced Feature Decision

### Selected Option

Option D: Component click event interaction.

### Why we chose this Option

This feature is already implemented in our dashboard and directly supports the main user journey: exploring map locations and immediately seeing actionable details for selected programs.

### Implemented Behavior

When a user clicks a map pin, the app treats that click as an interaction input and updates downstream outputs in real time.

Triggered output updates include:

1. Program details panel:
    - Program name, time of operation, address, meal cost, and program status.
2. Contact panel:
    - Contact email and phone number.
3. Service attributes:
    - Whether the program provides meals, hampers, and wheelchair accessibility.

This satisfies the M4 advanced feature requirement by using an output component (map markers) as a reactive input that filters the selected-row state and updates other UI components.
