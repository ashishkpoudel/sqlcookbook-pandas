import pandas as pd

employee_df = pd.read_csv(
  "/Users/ashish/Documents/pandas-exercises/data/employee.csv",
  dtype={
    "empno": int,
    "ename": str,
    "job": str,
    "mgr": str,
    "hiredate": str,
    "sal": float,
    "comm": float,
    "deptno": pd.Int64Dtype(),
    "notes": str
  }
)