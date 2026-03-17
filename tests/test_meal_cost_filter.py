import pandas as pd
from src.app import filter_by_meal_cost
from pathlib import Path  # changed from anyio to pathlib
import ibis
import pytest


PARQUET_PATH = Path("./data/processed/food_programs.parquet")

if not PARQUET_PATH.exists():
    PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)
    url = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/free-and-low-cost-food-programs/records?limit=100"
    raw = pd.read_json(url)
    df_init = pd.json_normalize(raw["results"])
    df_init.to_parquet(PARQUET_PATH, index=False)
    print(f"Parquet file created at {PARQUET_PATH}")
else:
    print(f"Parquet file already exists at {PARQUET_PATH}")

con = ibis.duckdb.connect()
df = con.read_parquet(str(PARQUET_PATH))





def test_filter_by_meal_cost_free():
    """
    Check that selecting 'Free' returns only rows where meal_cost is 'Free'.

    """
    result = filter_by_meal_cost(df, "Free").execute()
    assert (result['meal_cost'].str.lower() == "free").all()



def test_filter_by_meal_cost_low_cost():
    """
    Check that selecting 'Low-cost' returns all rows that where mean_cost is not 'Free'.

    """
    result = filter_by_meal_cost(df, "Low-cost").execute()

    assert (result['meal_cost'].str.lower() != "free").all()



def test_filter_by_meal_cost_all():
    """
    Check that selecting 'All' returns all rows regardless of meal_cost.
    
    """
    result = filter_by_meal_cost(df, "All").execute()
    assert len(result) == len(df.execute())
