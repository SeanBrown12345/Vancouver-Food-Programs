
from anyio import Path

from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import ipyleaflet

AI_AVAILABLE = True
AI_ERROR = ""

try:
    from dotenv import load_dotenv
    from querychat import QueryChat
    load_dotenv()
except Exception as e:
    AI_AVAILABLE = False
    AI_ERROR = str(e)

url = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records?limit=100"
df = pd.read_json(url)
df = pd.json_normalize(df["results"])

meal_cost_choices = ["All", "Free", "Low-cost"]
area_choices = sorted([str(x) for x in df["local_areas"].dropna().unique()])

qc = None
if AI_AVAILABLE:
    try:
        qc = QueryChat(df, "food_programs", client="openai/gpt-4.1")
    except Exception as e:
        AI_AVAILABLE = False
        AI_ERROR = str(e)

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
    padding: 0px !important;
    height: 100%;
    overflow: hidden !important;
}
#mainnavset { margin-left: 6px !important; }
.collapse-toggle[aria-expanded="true"] .collapse-icon { fill: white !important; }
.collapse-toggle[aria-expanded="false"] .collapse-icon { fill: black !important; }
.navbar {
    background-color: #0f3057 !important;
    color: white !important;
    padding: 0.75rem 1.25rem !important;
    font-size: 1.2rem !important;
    font-weight: 700;
    letter-spacing: 0.5px;
    border-radius: 0 0 16px 16px;
    margin-bottom: 1rem;
}
.panel_title {
    background-color: #0f3057;
    color: white;
    padding: 1rem 1.5rem;
    font-size: 1.4rem;
    font-weight: 900;
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
.shiny-options-group { margin-top: 4px; }
.sidebar {
    background-color: #272c32 !important;
    border-right: 1px solid #dde6ed;
    color: #fcfcfc !important;
    border-radius: 0px 8px 8px 0px !important;
}
.sidebar .form-control, .sidebar .form-select {
    border-radius: 8px !important;
    border: 1px solid #ccd6dd !important;
}
.sidebar label {
    font-weight: 600;
    color: #0f3057;
}
.card {
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.card_header {
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: #0f3057 !important;
    border-bottom: 1px solid #eef3f7;
    padding-bottom: 0.5rem !important;
    border-radius: 8px;
}
.card-body {
    padding: 1rem !important;
    border-radius: 8px;
    background-color: transparent !important;
}
.value-box {
    border-radius: 14px !important;
    background: linear-gradient(135deg, #00b4d8, #0077b6);
    color: white !important;
    box-shadow: 0 4px 14px rgba(0, 119, 182, 0.3);
}
.value-box:nth-child(2) { background: linear-gradient(135deg, #2a9d8f, #1b6f63); }
.value-box:nth-child(3) { background: linear-gradient(135deg, #f4a261, #e76f51); }
.value-box h6 {
    margin-bottom: 0.2rem !important;
    font-size: 0.8rem !important;
    opacity: 0.9;
}
.value-box .value-box-value {
    font-size: 1.3rem !important;
    font-weight: 700;
}
.bslib-sidebar-layout.main { padding: 0 !important; }
.leaflet-container { border-radius: 16px !important; }
h4 {
    font-size: 1.05rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #0f3057;
}
h2 { font-weight: 700; }
.control-label {
    color: #d0d2d6 !important;
    font-size: 1rem !important;
}
.main {
    padding: 0px !important;
    height: 100vh;
    max-height: 100vh;
    overflow-y: hidden;
    box-sizing: border-box;
}
.navset-card-pill {
    border-radius: 0px !important;
    background-color: red !important;
}
.tab-content { height: 100%; }
span { color: #8a8d93 !important; }
p {
    margin-bottom: 0.4rem;
    line-height: 1.4;
}
.input-select {
    background-color: #ffffff !important;
    border: 1px solid #ccd6dd !important;
    color: #0f3057 !important;
}
hr {
    border-top: 1px solid #ffff;
    margin: 0px !important;
}
.sidebar hr {
    color: #ffffff;
    margin: 0px !important;
}
._locations {
    background-color: #20a8d8 !important;
    color: white !important;
}
._programs {
    background-color: #fec106 !important;
    color: white !important;
}
._accessibility {
    background-color: #f86c6b !important;
    color: white !important;
}
.bslib-grid { margin-top: 8px !important; }
    """),

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
                ],
            ),
            open="desktop",
        ),

        ui.navset_card_pill(
            ui.nav_panel(
                "Dashboard",
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
                        full_screen=True,
                    ),

                    ui.layout_columns(
                        ui.card(
                            ui.card_header("Program Details"),
                            ui.output_ui("selected_details"),
                            full_screen=True,
                        ),
                        ui.card(
                            ui.card_header("Contact Information"),
                            ui.output_ui("contact_info"),
                            full_screen=True,
                        ),
                        col_widths=[12],
                    ),
                    col_widths=[8, 4],
                ),
            ),

            ui.nav_panel(
                "AI Explorer",
                ui.layout_columns(
                    ui.value_box("Total Locations", ui.output_text("ai_total_locations"), class_="_locations"),
                    ui.value_box("Free Programs (%)", ui.output_text("ai_free_prop"), class_="_programs"),
                    fill=False,
                    height="100px",
                ),

                ui.layout_columns(
                    ui.card(
                        ui.output_ui("ai_panel"),
                        full_screen=True,
                    ),

                    ui.layout_columns(
                        ui.download_button("downloadData", "Download"),
                        ui.card(
                            ui.card_header("Filtered Data"),
                            ui.output_data_frame("ai_data_table"),
                        ),
                        col_widths=[12],
                    ),

                    col_widths=[6, 6],
                ),
            ),

            id="mainnavset",
        ),
    ),
)


def server(input, output, session):
    qc_vals = qc.server() if AI_AVAILABLE and qc is not None else None
    selected_row = reactive.Value(None)

    @reactive.calc
    def filtered_df():
        dff = df.dropna(subset=["latitude", "longitude"]).copy()

        if input.meal_cost() != "All":
            if input.meal_cost() == "Free":
                dff = dff[dff["meal_cost"].astype(str).str.lower() == "free"]
            else:
                dff = dff[
                    dff["meal_cost"].astype(str).str.lower().str.contains("low cost")
                    | dff["meal_cost"].astype(str).str.startswith("$")
                ]

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
                draggable=False,
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
            ui.p(ui.strong("Wheelchair Accessible: "), row.get("wheelchair_accessible", "")),
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
            ui.p(ui.strong("Phone Number: "), phone if pd.notna(phone) else "Not available"),
        )

    @output
    @render.ui
    def ai_panel():
        if AI_AVAILABLE and qc is not None:
            return qc.ui()

        return ui.div(
            ui.h4("AI Explorer unavailable"),
            ui.p("The rest of the app still works normally."),
            ui.p("Reason:"),
            ui.pre(AI_ERROR if AI_ERROR else "Missing QueryChat / OpenAI configuration."),
        )

    @reactive.calc
    def ai_df():
        if not AI_AVAILABLE or qc_vals is None:
            return df.iloc[0:0]
        dff = qc_vals.df()
        if dff is None:
            return df.iloc[0:0]
        return dff

    @output
    @render.data_frame
    def ai_data_table():
        return ai_df()

    @output
    @render.text
    def ai_total_locations():
        return str(len(ai_df()))

    @output
    @render.text
    def ai_free_prop():
        dff = ai_df()
        if len(dff) == 0:
            return "0%"
        if "meal_cost" not in dff.columns:
            return "0%"
        return f"{(dff['meal_cost'].astype(str).str.lower() == 'free').mean():.1%}"

    @render.download(filename="filtered_vancouver_food_programs.csv")
    async def downloadData():
        dff = ai_df()
        yield dff.to_csv(index=False)


app_dir = Path(__file__).parent
app = App(app_ui, server, static_assets=app_dir / "www")
