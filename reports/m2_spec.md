# Milestone 2 Spec (v0.2.0)

## 2.1 Updated Job Stories

| # | Job Story | Status | Notes |
|---|-----------|--------|------|
| 1 | When I use the dashboard, I want to filter food programs by meal cost, so I can focus on options that match my budget. | ✅ Implemented | Uses the “Meal cost” dropdown (`meal_cost`). |
| 2 | When I explore food programs, I want to filter by local area, so I can find supports near where I live. | ✅ Implemented | Uses the “Local Area” multi-select (`area`). |
| 3 | When I explore food programs, I want to filter by features, so I can find programs with the services I need. | ✅ Implemented | Uses the “Features” checkbox group (`features`). |
| 4 | When I click a location on the map, I want to see program details and contact info, so I can decide where to go and how to reach them. | ✅ Implemented | Clicking a marker updates details and contact panels. |

---

## 2.2 Component Inventory

| ID | Type | Shiny widget / renderer | Depends on | Job story |
|----|------|--------------------------|------------|----------|
| meal_cost | Input | `ui.input_select()` | — | #1 |
| area | Input | `ui.input_selectize(multiple=True)` | — | #2 |
| features | Input | `ui.input_checkbox_group()` | — | #3 |
| filtered_df | Reactive calc | `@reactive.calc` | meal_cost, area, features | #1, #2, #3, #4 |
| selected_row | Reactive value | `reactive.Value(None)` | map click | #4 |
| total_locations | Output | `@render.text` | filtered_df | #1 |
| free_prop | Output | `@render.text` | filtered_df | #1 |
| accessibility_prop | Output | `@render.text` | filtered_df | #3 |
| map | Output | `@render_widget` | filtered_df | #4 |
| selected_details | Output | `@render.ui` | selected_row | #4 |
| contact_info | Output | `@render.ui` | selected_row | #4 |

> Note: 11 components listed (>= 8 required for a 4-person team; >= 2 inputs and >= 2 outputs satisfied).

---

## 2.3 Reactivity Diagram

```mermaid
flowchart TD
  A[/meal_cost/] --> F{{filtered_df}}
  B[/area/] --> F
  C[/features/] --> F

  F --> O1([total_locations])
  F --> O2([free_prop])
  F --> O3([accessibility_prop])
  F --> O4([map])

  O4 --> V([selected_row])
  V --> D([selected_details])
  V --> CI([contact_info])
````

---

## 2.4 Calculation Details

### `filtered_df` (@reactive.calc)

* **Inputs:** `meal_cost`, `area`, `features`
* **What it does:** Starts from the City of Vancouver food program dataset, removes rows without latitude/longitude, then filters the data based on selected meal cost, selected local areas, and selected program features (delivery, hampers, takeout, wheelchair access).
* **Used by outputs:** `total_locations`, `free_prop`, `accessibility_prop`, `map`

---

### `selected_row` (reactive.Value)

* **Inputs:** Map marker click event
* **What it does:** Stores the selected program row when a user clicks on a map marker.
* **Used by outputs:** `selected_details`, `contact_info`

---

### `total_locations` (@render.text)

* **Inputs:** `filtered_df`
* **What it does:** Counts the number of filtered programs and displays it as a summary metric.

---

### `free_prop` (@render.text)

* **Inputs:** `filtered_df`
* **What it does:** Calculates the percentage of filtered programs that are free.

---

### `accessibility_prop` (@render.text)

* **Inputs:** `filtered_df`
* **What it does:** Calculates the percentage of filtered programs that offer wheelchair accessibility.

---

### `map` (@render_widget)

* **Inputs:** `filtered_df`
* **What it does:** Displays an interactive ipyleaflet map with markers representing all filtered programs.

---

### `selected_details` (@render.ui)

* **Inputs:** `selected_row`
* **What it does:** Displays detailed information about the selected food program.

---

### `contact_info` (@render.ui)

* **Inputs:** `selected_row`
* **What it does:** Displays the contact email and phone information (if available) for the selected program.
