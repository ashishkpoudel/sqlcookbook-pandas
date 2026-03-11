import pandas as pd

new_salary_df = pd.read_csv(
    "/Users/ashish/Documents/pandas-exercises/data/new_salary.csv",
    dtype={
        "deptno": pd.Int64Dtype(),
        "sal": float,
    }
)
