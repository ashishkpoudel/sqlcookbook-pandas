import pandas as pd

employee_bonus_df = pd.read_csv(
  "/Users/ashish/Documents/pandas-exercises/data/employee_bonus.csv",
  dtype={
    "empno": int,
    "received": str,
    "type": int
  }
)
