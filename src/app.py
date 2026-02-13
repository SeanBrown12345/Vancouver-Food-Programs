from shiny import App, ui

# UI
app_ui = ui.page_fillable(
    ui.panel_title("Vancouver Food Programs"),
    ui.layout_sidebar(
        ui.sidebar("sidebar inputs", open="desktop"),
        ui.layout_columns(
            ui.value_box("Total Locations", "Value 1"),
            ui.value_box("Open Locations", "Value 2"),
            ui.value_box("Free vs Low Cost", "Value 3"),
            fill=False,
        ),

    ui.layout_columns(
        ui.card(
            ui.card_header("Location Map"),
            full_screen=True
        ),
        ui.div(
            ui.card(
                ui.card_header("Programs by Area"), full_screen=True,
            ),
            ui.card(
                ui.card_header("Takeout vs Delivery"), full_screen=True         
            ),
            style="display: flex; flex-direction: column; gap: 1rem;"
        ),
        col_widths=[8, 4] )
    )
)


# Server
def server(input, output, session):
    pass


# Create app
app = App(app_ui, server)