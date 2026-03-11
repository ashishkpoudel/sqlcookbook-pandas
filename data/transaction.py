import pandas as pd

transaction_df = pd.read_csv(
    "/Users/ashish/Documents/pandas-exercises/data/transaction.csv",
    dtype={
        "id": int,
        "amount": float,
        "tr": str
    }
)
