import pandas as pd
from app import filter_by_meal_cost

url = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records?limit=100"
df = pd.read_json(url)
df = pd.json_normalize(df["results"])

def test_filter_by_meal_cost_free():
    """
    Check that selecting 'Free' returns only rows where meal_cost is 'Free'.

    """
    result = filter_by_meal_cost(df, "Free")

    assert all(result["meal_cost"] == "Free")

def test_filter_by_meal_cost_low_cost():
    """
    Check that selecting 'Low-cost' returns all rows that where mean_cost is not 'Free'.

    """
    result = filter_by_meal_cost(df, "Low-cost")

    assert all(result["meal_cost"] != "Free")

def test_filter_by_meal_cost_all():
    """
    Check that selecting 'All' returns all rows regardless of meal_cost.
    
    """
    result = filter_by_meal_cost(df, "All")

    assert len(result) == len(df)
