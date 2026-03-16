import pandas as pd

transaction_df = pd.read_csv(
    "/Users/ashish/Documents/pandas-exercises/data/transaction_full.csv",
    dtype={
        "trx_id": pd.Int64Dtype(),
        "trx_date": pd.StringDtype(),
        "trx_count": pd.Int64Dtype()
    }
)
