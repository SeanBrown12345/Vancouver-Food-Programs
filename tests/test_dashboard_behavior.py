from playwright.sync_api import Page, expect

APP_URL = "https://019c9c40-a7bf-b588-73bc-bddb7328a53a.share.connect.posit.cloud"


def test_dashboard_tab_shows_summary_and_map(page: Page):
    """Checks that the Dashboard tab displays the overview summary and map, which matters because users rely on the landing view for a quick scan of food program availability."""
    page.goto(APP_URL, wait_until="networkidle")

    dashboard_tab = page.get_by_role("tab", name="Dashboard").first
    expect(dashboard_tab).to_be_visible()
    dashboard_tab.click()

    expect(page.locator("p", has_text="Total Locations").first).to_be_visible()
    expect(page.get_by_text("Location Map").first).to_be_visible()


def test_filter_panel_labels_are_rendered(page: Page):
    """Checks that the main filter panel renders its key controls, which matters because users need these inputs to narrow results by cost, area, and program features."""
    page.goto(APP_URL, wait_until="networkidle")

    expect(page.get_by_text("Meal Cost").first).to_be_visible()
    expect(page.get_by_text("Local Area").first).to_be_visible()
    expect(page.get_by_text("Features").first).to_be_visible()


def test_ai_explorer_tab_opens_and_shows_content(page: Page):
    """Checks that the AI Explorer tab opens and shows its main content, which matters because the AI workflow is one of the app's main user-facing features."""
    page.goto(APP_URL, wait_until="networkidle")

    ai_tab = page.get_by_role("tab", name="AI Explorer").first
    expect(ai_tab).to_be_visible()
    ai_tab.click()

    expect(page.get_by_text("Filtered Data").first).to_be_visible()