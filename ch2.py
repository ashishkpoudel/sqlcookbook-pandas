import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import random
    from data.employee import employee_df
    return employee_df, np, pd, random


@app.cell
def _(employee_df):
    """
    Use compination of and or not to satisy multiple conditions
    """

    employee_mask = (employee_df["deptno"] == 10) & ((employee_df["comm"].notna()) | employee_df["sal"] <= 2000)
    employee_df[employee_mask]
    return


@app.cell
def _(employee_df):
    """
    retrieve a subset of columns from dataset
    """

    employee_df[["ename", "job", "hiredate"]]
    return


@app.cell
def _(employee_df):
    """
    rename existing columns
    """

    employee_df.rename(columns={"sal": "salary", "comm": "commission"})[["salary", "commission"]]
    return


@app.cell
def _(employee_df):
    """
    use pipe to combine multiple modifications to pandas dataframe
    use assign to add new columns
    this avoids from creating too many variables or having to mutate one single variable in every line
    """

    (
      employee_df
        .pipe(lambda df: df[df["deptno"] == 10])
        .pipe(lambda df: df.rename(columns={"empno": "emp_no", "ename": "employee_name", "sal": "salary", "comm": "commission"}))
        .assign(commission = lambda df: df["commission"].fillna(0))
        .assign(**{"employee message": lambda df: df["employee_name"] + " works as a " + df["job"]})
        .pipe(lambda df: df[["emp_no", "employee_name", "commission", "salary", "employee message"]])
    )
    return


@app.cell
def _(employee_df):
    """
    compute value based on conditional logic and create a new column
    """

    def sal_status(row: dict):
      if row["sal"] <= 2000:
        return "underpaid"

      if row["sal"] >= 4000:
        return "overpaid"

      return "ok"


    (
      employee_df
        .assign(status = lambda df: df.apply(sal_status, axis=1))
    )
    return


@app.cell
def _(employee_df, random):
    """
    select random records
    """

    (
      employee_df
        .pipe(lambda df: df.sample(n=3, random_state=random.randint(0, 100)))
        .pipe(lambda df: df[["ename", "job"]])
    )
    return


@app.cell
def _(employee_df):
    """
    equivalent of where-in query in pandas
    """

    (
      employee_df
        .pipe(lambda df: df[df["deptno"].isin([10, 20])])
    )
    return


@app.cell
def _(employee_df):
    """
    retun query results in specific order
    """

    (
      employee_df
        .pipe(lambda df: df[df["deptno"] == 10])
        .pipe(lambda df: df.sort_values(["ename", "sal"], ascending=True))
    )
    return


@app.cell
def _(employee_df):
    """
    multi-column ordering
    """

    (
      employee_df
        .pipe(lambda df: df.sort_values(["ename", "sal"], ascending=[True, False]))
    )
    return


@app.cell
def _(employee_df, pd):
    """
    sort the results by specific parts of string
    """

    def drop_private_columns(df: pd.DataFrame):
      columns_private_mask = df.columns.str.startswith("_")
      columns_private_list = list(df.columns[columns_private_mask])

      return df.drop(columns=columns_private_list)

    employee_df["_ename_sort_key"] = employee_df["ename"].apply(
      lambda ename: ename[:3]
    )

    (
      employee_df
        .pipe(lambda df: df.sort_values(["_ename_sort_key"], ascending=[True]))
        .pipe(lambda df: drop_private_columns(df))
    )
    return


@app.cell
def _(employee_df):
    """
    sort the results by specific parts of string more compact approach
    """

    (
      employee_df
        .assign(_ename_sort_key = lambda df: df["ename"].str[:3] )
        .sort_values(["_ename_sort_key"], ascending=[True])
        .drop(columns=["_ename_sort_key"])
    )
    return


@app.cell
def _(employee_df):
    """
    sort data where records for null are either (first or last)
    """

    (
      employee_df
        .sort_values(["comm", "hiredate"], ascending=[True, False], na_position="first")
    )
    return


@app.cell
def _(employee_df, np):
    """
    sort based on some conditional logic. For example, if job is SALESMAN, you want to sort on comm;
    otherwise, you want to sort by sal
    """

    (
      employee_df
        .assign(_sort_key = lambda df: np.where(df["job"] == "SALESMAN", df["comm"], df["sal"]))
        .sort_values(["_sort_key"], ascending=[True])
    )
    return


@app.cell
def _(employee_df):
    """
    Find total salary in each department along with employee count
    """

    (
        employee_df
            .groupby(["deptno"])
            .agg(
                total_salary=("sal", "sum"),
                employee_count=("deptno", "count")
            )
    )
    return


if __name__ == "__main__":
    app.run()
