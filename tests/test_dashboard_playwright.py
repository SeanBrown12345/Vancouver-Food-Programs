
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
    
    delivery_checkbox = page.locator('input[value="Delivery Available"]')
    assert delivery_checkbox.is_visible()
    
    delivery_checkbox.check()
    page.wait_for_timeout(1000)
    
    program_cards = page.locator('[data-testid="program-card"]')
    assert program_cards.count() > 0

def test_feature_checkbox_hampers(page, local_app):
    """
    Verify that checking "Provides Hampers" checkbox filters results.
    """
    page.goto(local_app.url)
    
    hampers_checkbox = page.locator('input[value="Provides Hampers"]')
    assert hampers_checkbox.is_visible()
    
    hampers_checkbox.check()
    page.wait_for_timeout(1000)
    
    program_cards = page.locator('[data-testid="program-card"]')
    assert program_cards.count() > 0

def test_feature_checkbox_takeout(page, local_app):
    """
    Verify that checking "Takeout Available" checkbox filters results.
    """
    page.goto(local_app.url)
    
    takeout_checkbox = page.locator('input[value="Takeout Available"]')
    assert takeout_checkbox.is_visible()
    
    takeout_checkbox.check()
    page.wait_for_timeout(1000)
    
    program_cards = page.locator('[data-testid="program-card"]')
    assert program_cards.count() > 0

def test_feature_checkbox_wheelchair(page, local_app):
    """
    Verify that checking "Wheelchair Accessible" checkbox filters results.
    """
    page.goto(local_app.url)
    
    wheelchair_checkbox = page.locator('input[value="Wheelchair Accessible"]')
    assert wheelchair_checkbox.is_visible()
    
    wheelchair_checkbox.check()
    page.wait_for_timeout(1000)
    
    program_cards = page.locator('[data-testid="program-card"]')
    assert program_cards.count() > 0





