import pandas as pd

project_df = pd.read_csv(
    "/Users/ashish/Documents/pandas-exercises/data/project.csv",
    dtype={
        "project_id": pd.Int64Dtype(),
        "start_date": pd.StringDtype(),
        "end_date": pd.StringDtype()
    }
)
