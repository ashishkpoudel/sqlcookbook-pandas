import pandas as pd

department_accident_df = pd.read_csv(
    "/Users/ashish/Documents/pandas-exercises/data/department_accident.csv",
    dtype={
        "deptno": int,
        "accident": str
    }
)
