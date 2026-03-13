
import pytest
pytestmark = pytest.mark.parametrize("local_app", ["../src/app.py"], indirect=True)

def test_meal_cost_filter_options(page, local_app):
    """
    Verify that the selections in the "Meal Cost" filter only display "All", "Free" and "Low Cost" options.
    
    """
    page.goto(local_app.url)

    options = page.locator('#meal_cost option').all_inner_texts()

    assert options == ["All", "Free", "Low-cost"]



def test_feature_checkbox_delivery(page, local_app):
    """
    Verify that checking "Delivery Available" filters results.
    """
    page.goto(local_app.url)
    page.wait_for_timeout(2000)

    before = int(page.locator("#total_locations").text_content().strip())

    page.locator('input[value="Delivery Available"]').check()
    page.wait_for_timeout(1000)

    after = int(page.locator("#total_locations").text_content().strip())
    assert after <= before


def test_feature_checkbox_hampers(page, local_app):
    """
    Verify that checking "Provides Hampers" checkbox filters results.
    """
    page.goto(local_app.url)
    page.wait_for_timeout(2000)

    before = int(page.locator("#total_locations").text_content().strip())

    page.locator('input[value="Provides Hampers"]').check()
    page.wait_for_timeout(1000)

    after = int(page.locator("#total_locations").text_content().strip())
    assert after <= before


def test_feature_checkbox_takeout(page, local_app):
    """
    Verify that checking "Takeout Available" checkbox filters results.
    """
    page.goto(local_app.url)
    page.wait_for_timeout(2000)

    before = int(page.locator("#total_locations").text_content().strip())

    page.locator('input[value="Takeout Available"]').check()
    page.wait_for_timeout(1000)

    after = int(page.locator("#total_locations").text_content().strip())
    assert after <= before


def test_feature_checkbox_wheelchair(page, local_app):
    """
    Verify that checking "Wheelchair Accessible" checkbox filters results.
    """
    page.goto(local_app.url)
    page.wait_for_timeout(2000)

    before = int(page.locator("#total_locations").text_content().strip())

    page.locator('input[value="Wheelchair Accessible"]').check()
    page.wait_for_timeout(1000)

    after = int(page.locator("#total_locations").text_content().strip())
    assert after <= before