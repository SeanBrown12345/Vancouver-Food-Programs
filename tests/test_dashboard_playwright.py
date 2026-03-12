
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
   