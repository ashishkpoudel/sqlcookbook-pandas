import pandas as pd

department_df = pd.read_csv(
  "/Users/ashish/Documents/pandas-exercises/data/department.csv",
  dtype={
    "deptno": int,
    "dname": str,
    "loc": str,
    "notes": str
  }  
)
