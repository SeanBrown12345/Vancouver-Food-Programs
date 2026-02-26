from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import ipyleaflet


url = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records?limit=100"
df = pd.read_json(url)
df = pd.json_normalize(df["results"])


meal_cost_choices = ["All"] + sorted([str(x) for x in df["meal_cost"].dropna().unique()])
area_choices = ["All"] + sorted([str(x) for x in df["local_areas"].dropna().unique()])


app_ui = ui.page_fillable(
ui.tags.style("""
    html, body {
        font-size: 14px;
        background: linear-gradient(135deg, #f4f9f9 0%, #e8f1f2 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #1f2d3d;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    .panel_title {
        background-color: #0f3057;
        color: white;
        padding: 1rem 1.5rem;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        border-radius: 0 0 16px 16px;
        margin-bottom: 1rem;
    }

    .navbar, .panel-title {
        background-color: #ffffff !important;
        background: #0f3057 !important;
        color: white !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 600;
        letter-spacing: 0.5px;
        
    }


    .sidebar {
        background-color: #ffffff !important;
        border-right: 1px solid #dde6ed;
        padding: 1rem !important;
        border-radius: 16px !important;
        
    }

    .sidebar .form-control,
    .sidebar .form-select {
        border-radius: 8px !important;
        border: 1px solid #ccd6dd !important;
    }

    .sidebar label {
        font-weight: 600;
        color: #0f3057;
    }

    .card {
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    }

    .card_header {
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: #0f3057 !important;
        border-bottom: 1px solid #eef3f7;
        padding-bottom: 0.5rem !important;
    }

    .card-body {
        padding: 1rem !important;
    }

    .value-box {
        border-radius: 14px !important;
        background: linear-gradient(135deg, #00b4d8, #0077b6);
        color: white !important;
        box-shadow: 0 4px 14px rgba(0, 119, 182, 0.3);
    }

    .value-box:nth-child(2) {
        background: linear-gradient(135deg, #2a9d8f, #1b6f63);
    }

    .value-box:nth-child(3) {
        background: linear-gradient(135deg, #f4a261, #e76f51);
    }

    .value-box h6 {
        margin-bottom: 0.2rem !important;
        font-size: 0.8rem !important;
        opacity: 0.9;
    }

    .value-box .value-box-value {
        font-size: 1.3rem !important;
        font-weight: 700;
    }

    .leaflet-container {
        border-radius: 16px !important;
    }

    h4 {
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: #0f3057;
    }

    p {
        margin-bottom: 0.4rem;
        line-height: 1.4;
    }

    hr {
        border-top: 1px solid #e0e6eb;
    }
    """),
    ui.panel_title("Vancouver Food Programs"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("meal_cost", "Meal cost", choices=meal_cost_choices, selected="All"),
            ui.input_select("area", "Local Area", choices=area_choices, selected="All"),
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
            ui.value_box("Total Locations", ui.output_text("total_locations")),
            ui.value_box("Free Programs (%)", ui.output_text("free_prop")),
            ui.value_box("Accessibility (%)", ui.output_text("accessibility_prop")),
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
                ui.card_header(ui.strong("Program Details")),
                ui.output_ui("selected_details"),
                full_screen=True
            ),
            ui.card(
                ui.card_header(ui.strong("Contact Information")),
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
        dff = df.dropna(subset=["latitude", "longitude"])

        if input.meal_cost() != "All":
            dff = dff[dff["meal_cost"].astype(str) == input.meal_cost()]

        if input.area() != "All":
            dff = dff[dff["local_areas"].astype(str) == input.area()]

        features = input.features()

        if "Delivery Available" in features:
            dff = dff[dff["delivery_available"].astype(str) == "Yes"]

        if "Provides Hampers" in features:
            dff = dff[dff["provides_hampers"].astype(str) == "True"]

        if "Takeout Available" in features:
            dff = dff[dff["takeout_available"].astype(str) == "Yes"]

        if "Wheelchair Accessible" in features:
            dff = dff[dff["wheelchair_accessible"].astype(str) == "Yes"]

        return dff

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

        for _, row in dff.iterrows():
            marker = ipyleaflet.Marker(
                location=(float(row["latitude"]), float(row["longitude"])),
                title=str(row.get("program_name", "")),
                draggable=False
            )

            def handle_click(event=None, row=row, **kwargs):
                selected_row.set(row.to_dict())

            marker.on_click(handle_click)
            m.add_layer(marker)

        return m

    @output
    @render.ui
    def selected_details():
        row = selected_row.get()

        if row is None:
            return ui.p("Click a location on the map.")

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

app = App(app_ui, server)