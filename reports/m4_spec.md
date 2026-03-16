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
| Feedback prioritization issue | GitHub issue titled M4 Feedback Prioritization |
| Feedback addressed | Instructor and TA feedback items implemented; peer items documented |
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
2. Add a DuckDB connection through Ibis so the parquet file can be queried lazily.
3. Move filter logic to the Ibis query layer inside `@reactive.calc` so input controls apply filters before rows are loaded into a DataFrame.
4. Materialize data only after filters are applied by calling `execute()` at the end of the reactive calculation.

### Expected result:

- Filtering will happen at the database/query level before rows are loaded into a pandas DataFrame.
- The map and summary outputs will render from already-filtered rows.
- Existing UI behavior should remain the same while reducing unnecessary in-memory processing.

### Validation plan:

- Confirm that meal cost, local area, and feature filters return expected row subsets after the migration.
- Confirm that map points and summary metrics update correctly for representative filter combinations.
- Run the existing test suite after migration to ensure everything works well.

## 6. Testing

We will implement three Playwright tests to cover key user-facing dashboard behaviors.

- A dashboard rendering test to confirm that the main dashboard view displays the expected summary outputs and map.
- A Meal Cost options test to confirm that the Meal Cost filter contains only the intended options: All, Free, and Low-cost.
- Feature checkbox behavior tests to confirm that selecting Delivery Available, Provides Hampers, Takeout Available, and Wheelchair Accessible correctly updates the displayed results.

We will also include a unit test for `filter_by_meal_cost` to verify that selecting All returns the full dataset, selecting Free returns only free programs, and selecting Low-cost excludes free programs. This will ensure that the meal cost filtering logic behaves as intended.

### Test Execution

README will document a single command entry point for tests in clean environments, and tests must pass before release tagging.

Planned command:
- python -m pytest

## 7. Feedback Prioritization and Resolution

To ensure that the most important issues are addressed during Milestone 4, we will organize and prioritize all feedback received from the instructor, TA, and peers.

Process:
- Create a GitHub issue titled M4 Feedback Prioritization.
- Gather all feedback from the instructor, TA, and peers in that issue.
- Categorize each item as either Critical or Non-critical.
- Resolve all critical instructor and TA feedback items through pull requests.
- Address additional non-critical instructor and TA feedback as time permits.
- Document peer feedback in the prioritization issue and implement it only if it is reclassified as critical or fits within the team's available capacity.
- Ensure that each team member resolves at least one feedback item.

### Feedback Work Plan

| Feedback Item | Source | Priority | Owner |
|---|---|---|---|
| Map losing points with certain clicks (To achieve this we moved from ipyleaflet to plotly map)| Instructor/Peer | Critical | Sean |
| Move download button to same card as data frame | Instructor | Critical | Daniel |
| remove @output calls | Instructor | Non-critical | Jennifer |
| Increase Card Header size | Peer | Non-critical | Aitong |
