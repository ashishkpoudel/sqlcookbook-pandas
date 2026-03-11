import pandas as pd

sales_df = pd.read_csv(
    "/Users/ashish/Documents/pandas-exercises/data/sales.csv",
    dtype={
        "date": str,
        "sales": float,
    }
)
