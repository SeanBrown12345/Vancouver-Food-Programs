from anyio import Path

from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import ipyleaflet


url = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records?limit=100"
df = pd.read_json(url)
df = pd.json_normalize(df["results"])


meal_cost_choices = ["All"] + sorted([str(x) for x in df["meal_cost"].dropna().unique()])
area_choices = sorted([str(x) for x in df["local_areas"].dropna().unique()])


app_ui = ui.page_fillable(
    ui.tags.link(href="styles.css", rel="stylesheet"),

    ui.layout_sidebar(
        ui.sidebar(
            ui.panel_title("Vancouver Food Programs"),
            ui.hr(),
            ui.input_select("meal_cost", "Meal cost", choices=meal_cost_choices, selected="All"),
            ui.hr(),
            ui.input_selectize("area", "Local Area", choices=area_choices, multiple=True),
            ui.hr(),
            ui.input_checkbox_group(
                "features",
                "Features",
                choices=[
                    "Delivery Available",
                    "Provides Hampers",
                    "Takeout Available",
                    "Wheelchair Accessible",
                ]
            ),
            open="desktop"
        ),

        ui.layout_columns(
            ui.value_box("Total Locations", ui.output_text("total_locations"), class_="_locations"),
            ui.value_box("Free Programs (%)", ui.output_text("free_prop"), class_="_programs"),
            ui.value_box("Accessibility (%)", ui.output_text("accessibility_prop"), class_="_accessibility"),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Location Map"),
                output_widget("map"),
                full_screen=True
            ),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Program Details"),
                    ui.output_ui("selected_details"),
                    full_screen=True
                ),
                ui.card(
                    ui.card_header("Contact Information"),
                    ui.output_ui("contact_info"),
                    full_screen=True
                ),
                col_widths=[12]
            ),
            col_widths=[8, 4]
        )
    )
)


def server(input, output, session):

    selected_row = reactive.Value(None)

    @reactive.calc
    def filtered_df():
        dff = df.dropna(subset=["latitude", "longitude"]).copy()

        if input.meal_cost() != "All":
            dff = dff[dff["meal_cost"].astype(str) == input.meal_cost()]

        selected_areas_raw = input.area()
        selected_areas = []
        if selected_areas_raw is not None:
            selected_areas = [str(x) for x in selected_areas_raw if str(x).strip() != ""]

        if len(selected_areas) > 0:
            dff = dff[dff["local_areas"].astype(str).isin(selected_areas)]

        features_raw = input.features()
        features = []
        if features_raw is not None:
            features = [str(x) for x in features_raw if str(x).strip() != ""]

        if "Delivery Available" in features:
            dff = dff[dff["delivery_available"].astype(str) == "Yes"]

        if "Provides Hampers" in features:
            dff = dff[dff["provides_hampers"].astype(str) == "True"]

        if "Takeout Available" in features:
            dff = dff[dff["takeout_available"].astype(str) == "Yes"]

        if "Wheelchair Accessible" in features:
            dff = dff[dff["wheelchair_accessible"].astype(str) == "Yes"]

        return dff

    @reactive.effect
    def _clear_selected_row_on_filter_change():
        filtered_df()
        selected_row.set(None)

    @output
    @render.text
    def total_locations():
        return str(len(filtered_df()))

    @output
    @render.text
    def free_prop():
        dff = filtered_df()
        if len(dff) == 0:
            return "0%"
        return f"{(dff['meal_cost'].astype(str).str.lower() == 'free').mean():.1%}"

    @output
    @render.text
    def accessibility_prop():
        dff = filtered_df()
        if len(dff) == 0:
            return "0%"
        accessible = dff["wheelchair_accessible"].astype(str).str.lower() == "yes"
        return f"{accessible.mean():.1%}"

    @output
    @render_widget
    def map():
        dff = filtered_df()
        m = ipyleaflet.Map(center=(49.2827, -123.1207), zoom=12)

        markers = []
        for _, row in dff.iterrows():
            marker = ipyleaflet.Marker(
                location=(float(row["latitude"]), float(row["longitude"])),
                title=str(row.get("program_name", "")),
                draggable=False
            )

            def handle_click(event=None, row=row, **kwargs):
                selected_row.set(row.to_dict())

            marker.on_click(handle_click)
            markers.append(marker)

        if len(markers) > 0:
            cluster = ipyleaflet.MarkerCluster(markers=markers)
            m.add_layer(cluster)

        return m

    @output
    @render.ui
    def selected_details():
        row = selected_row.get()

        if row is None:
            return ui.p("Select a location on the map to view program details.")

        return ui.div(
            ui.h4(row.get("program_name", "")),
            ui.p(row.get("description", "")),
            ui.hr(),
            ui.p(ui.strong("Organization: "), row.get("organization_name", "")),
            ui.p(ui.strong("Address: "), row.get("location_address", "")),
            ui.p(ui.strong("Meal Cost: "), row.get("meal_cost", "")),
            ui.p(ui.strong("Program Status: "), row.get("program_status", "")),
            ui.p(ui.strong("Provides Meals: "), row.get("provides_meals", "")),
            ui.p(ui.strong("Provides Hampers: "), row.get("provides_hampers", "")),
            ui.p(ui.strong("Delivery Available: "), row.get("delivery_available", "")),
            ui.p(ui.strong("Takeout Available: "), row.get("takeout_available", "")),
            ui.p(ui.strong("Wheelchair Accessible: "), row.get("wheelchair_accessible", ""))
        )

    @output
    @render.ui
    def contact_info():
        row = selected_row.get()

        if row is None:
            return ui.p("Select a location to view contact information.")

        email = row.get("signup_email", "Not available")
        phone = row.get("signup_phone_number", "Not available")

        return ui.div(
            ui.p(ui.strong("Email: "), email if pd.notna(email) else "Not available"),
            ui.p(ui.strong("Phone Number: "), phone if pd.notna(phone) else "Not available")
        )

app_dir = Path(__file__).parent
app = App(app_ui, server, static_assets=app_dir / "www")
