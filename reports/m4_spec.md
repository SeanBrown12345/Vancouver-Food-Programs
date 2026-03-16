# Milestone 4 Spec (v0.4.0)

## 1. Milestone Scope

This document specifies the final production-readiness work for the Vancouver Food Programs dashboard in Milestone 4. The scope includes performance hardening with parquet plus DuckDB query pushdown, one advanced feature implementation, behavior and unit testing, and structured resolution of instructor, TA, and peer feedback.

The M4 goal is to ship a stable, documented, and test-backed release on Posit Connect Cloud with clear team collaboration records in GitHub Issues, PRs, and release notes.

This specification is intentionally written as a design-before-code plan. It documents what the team intends to implement and verify during Milestone 4.

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

### Planned Behavior

When a user clicks a map pin, the app treats that click as an interaction input and updates downstream outputs in real time.

Planned output updates include:

1. Program details panel:
    - Program name, time of operation, address, meal cost, and program status.
2. Contact panel:
    - Contact email and phone number.
3. Service attributes:
    - Whether the program provides meals, hampers, and wheelchair accessibility.

This satisfies the M4 advanced feature requirement by using an output component (map markers) as a reactive input that filters the selected-row state and updates other UI components.

## 5. Converting pandas to Ibis with DuckDB

The dashboard data pipeline will be migrated from eager pandas filtering to query-first filtering with Ibis + DuckDB.

### Planned code changes:

1. Add parquet-backed storage in `data/processed/food_programs.parquet` so the app reads from a columnar file instead of repeatedly loading and filtering a full in-memory table.
2. Add DuckDB connection through Ibis:
3. Move filter logic to the Ibis query layer inside `@reactive.calc
4. Materialize data only after filters are applied by calling `execute()` at the end of the reactive calculation.

### Expected result:

- Filtering will happen at the database/query level before rows are loaded into a pandas DataFrame.
- The map and summary outputs will render from already-filtered rows.
- Existing UI behavior should remain the same while reducing unnecessary in-memory processing.

### Validation plan:

- Confirm that meal cost, local area, and feature filters return expected row subsets after the migration.
- Confirm that map points and summary metrics update correctly for representative filter combinations.
- Run the existing test suite after migration to ensure evrything works well.

