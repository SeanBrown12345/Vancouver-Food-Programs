from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import ipyleaflet

df = pd.read_csv("food_program_data.csv", sep=";")

df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

meal_cost_choices = ["All"] + sorted(
    [str(x) for x in df["Meal Cost"].dropna().unique()],
    key=lambda s: s.lower()
)

area_choices = ["All"] + sorted(
    [str(x) for x in df["Local Areas"].dropna().unique()]
)

app_ui = ui.page_fillable(
    ui.panel_title("Vancouver Food Programs"),

    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("meal_cost", "Meal cost",
                            choices=meal_cost_choices, selected="All"),
            ui.input_select("area", "Local Area",
                            choices=area_choices, selected="All"),
            ui.input_checkbox_group(
                "features",
                "Filter by features",
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
            ui.value_box("Free & Open (%)", ui.output_text("free_open_prop")),
            fill=False,
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Location Map"),
                output_widget("map"),
                full_screen=True
            ),

            ui.card(
                ui.card_header("Selected Program Details"),
                ui.output_ui("selected_details"),
                full_screen=True
            ),

            col_widths=[8, 4]
        )
    )
)

def server(input, output, session):

    selected_row = reactive.Value(None)
    @reactive.calc
    def filtered_df():
        dff = df.dropna(subset=["Latitude", "Longitude"])

        if input.meal_cost() != "All":
            dff = dff[dff["Meal Cost"].astype(str) == input.meal_cost()]

        if input.area() != "All":
            dff = dff[dff["Local Areas"].astype(str) == input.area()]

        features = input.features()

        if "Delivery Available" in features:
            dff = dff[dff["Delivery Available"].astype(str) == "Yes"]

        if "Provides Hampers" in features:
            dff = dff[dff["Provides Hampers"].astype(str) == "True"]

        if "Takeout Available" in features:
            dff = dff[dff["Takeout Available"].astype(str) == "Yes"]

        if "Wheelchair Accessible" in features:
            dff = dff[dff["Wheelchair Accessible"].astype(str) == "Yes"]

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
        return f"{(dff['Meal Cost'].astype(str).str.lower() == 'free').mean():.1%}"

    @output
    @render.text
    def free_open_prop():
        dff = filtered_df()
        if len(dff) == 0:
            return "0%"
        free = dff["Meal Cost"].astype(str).str.lower() == "free"
        open_mask = dff["Program Status"].astype(str).str.lower() == "open"
        return f"{(free & open_mask).mean():.1%}"

    @output
    @render_widget
    def map():
        dff = filtered_df()

        if len(dff) == 0:
            center = (49.2827, -123.1207)
        else:
            center = (
                float(dff["Latitude"].mean()),
                float(dff["Longitude"].mean())
            )

        m = ipyleaflet.Map(center=center, zoom=12)

        for _, row in dff.iterrows():

            marker = ipyleaflet.Marker(
                location=(float(row["Latitude"]), float(row["Longitude"])),
                title=str(row.get("Program Name", "")),
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
            ui.h4(row.get("Program Name", "")),
            ui.p(ui.strong("Organization: "),
                 row.get("Organization Name", "")),
            ui.p(ui.strong("Address: "),
                 row.get("Location Address", "")),
            ui.p(ui.strong("Meal Cost: "),
                 row.get("Meal Cost", "")),
            ui.p(ui.strong("Program Status: "),
                 row.get("Program Status", "")),
            ui.p(ui.strong("Provides Meals: "),
                 row.get("Provides Meals", "")),
            ui.p(ui.strong("Provides Hampers: "),
                 row.get("Provides Hampers", "")),
            ui.p(ui.strong("Delivery Available: "),
                 row.get("Delivery Available", "")),
            ui.p(ui.strong("Takeout Available: "),
                 row.get("Takeout Available", "")),
            ui.p(ui.strong("Wheelchair Accessible: "),
                 row.get("Wheelchair Accessible", "")),
            ui.hr(),
            ui.p(row.get("Description", ""))
        )

app = App(app_ui, server)