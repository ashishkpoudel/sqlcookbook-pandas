import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import numpy as np
    from typing import cast
    from data.employee import employee_df
    from data.department import department_df
    from data.employee_bonus import employee_bonus_df
    return department_df, employee_bonus_df, employee_df, pd


@app.cell
def _(department_df, employee_df, pd):
    """
    union all equivalent of sql
    union equivalent of sql is pd.concat with drop_duplicates()
    """

    employee_data = (
      employee_df
        .pipe(lambda df: df[df["deptno"] == 10])
        .assign(source = lambda df: "employee")
        .pipe(lambda df: df[["ename", "deptno", "source", "notes"]])
        .rename(columns={"ename": "ename_dname"})
    )

    department_data = (
      department_df
        .assign(source = lambda df: "department")
        .pipe(lambda df: df[["dname", "deptno", "source", "notes",]])
        .rename(columns={"dname": "ename_dname"})
    )


    (
      pd.concat([employee_data, department_data], ignore_index=True)
    )
    return


@app.cell
def _(department_df, employee_df, pd):
    """
    inner join
    if both dataframe has same column name they will appear with _x or _y suffix
    example: source_x from employee_data and source_y from department_data
    you can change the defult suffix to custom ones using: suffixes=('_emp', '_dept')
    """

    _employee_data = (
      employee_df
        .assign(source = lambda df: "employee")
        .pipe(lambda df: df[["ename", "deptno", "source", "notes"]])
    )

    _department_data = (
      department_df
        .assign(source = lambda df: "department")
        .pipe(lambda df: df[["dname", "deptno", "source", "notes"]])
    )

    (
      pd
        .merge(_employee_data, _department_data, left_on="deptno", right_on="deptno", how="inner")
        .pipe(lambda df: df[["ename", "deptno", "dname"]])
    )
    return


@app.cell
def _(department_df, employee_df):
    """
    return deptno from department if that do not exists in employee data
    """

    (
      department_df
        .pipe(
          lambda df:
          df[~df["deptno"].isin(employee_df["deptno"].unique())]
        )
    )
    return


@app.cell
def _(department_df, employee_bonus_df, employee_df):
    """
    you want to return all employees, the location of the department in which they work, and
    the date they received a bonus
    """

    (
      employee_df
        .merge(department_df, left_on="deptno", right_on="deptno", how="inner")
        .merge(employee_bonus_df, left_on="empno", right_on="empno", how="left")
        [["empno", "ename", "deptno", "dname", "received"]]
        .reset_index()
    )
    return


@app.cell
def _(department_df, employee_df):
    """
    return the name of each employee in department 10 along with the location of department
    """

    (
        employee_df
            .pipe(lambda df: df[df["deptno"].isin([10])])
            .merge(department_df, left_on="deptno", right_on="deptno", how="inner")
            .filter(["empno", "ename", "deptno", "dname"])
            .reset_index()
    )
    return


@app.cell
def _(employee_bonus_df, employee_df):
    """
    Method 1

    Find the sum of the salaries for employees in department 10 along with the sum of
    their bonuses. 

    Note: Some employees have more than one bonus, and the join between
    table EMP and table EMP_BONUS is causing incorrect values to be returned by the
    aggregate function SUM
    """

    def _calculate_bonus(row: dict):
        if row["type"] == 1:
            return 0.10 * row["sal"]

        if row["type"] == 2:
            return 0.20 * row["sal"]

        if row["type"] == 3:
            return 0.30 * row["sal"]

        return 0


    (
        employee_df
            .merge(employee_bonus_df, left_on="empno", right_on="empno", how="inner")
            .query("deptno == 10")
            .assign(bonus = lambda df: df.apply(_calculate_bonus, axis=1))
            .assign(total_salary = lambda df: df.drop_duplicates("empno")["sal"].sum())
            .assign(total_bonus = lambda df: df["bonus"].sum())
            .filter(["total_salary", "total_bonus"])
            .drop_duplicates()
            .reset_index()
    )
    return


@app.cell
def _(employee_bonus_df, employee_df):
    """
    Method 2

    Find the sum of the salaries for employees in department 10 along with the sum of
    their bonuses. 

    Note: Some employees have more than one bonus, and the join between
    table EMP and table EMP_BONUS is causing incorrect values to be returned by the
    aggregate function SUM
    """

    def _calculate_bonus(row: dict):
        if row["type"] == 1:
            return 0.10 * row["sal"]

        if row["type"] == 2:
            return 0.20 * row["sal"]

        if row["type"] == 3:
            return 0.30 * row["sal"]

        return 0


    (
        employee_df
            .query("deptno == 10")
            .assign(total_salary = lambda df: df["sal"].sum())
            .merge(employee_bonus_df, left_on="empno", right_on="empno", how="inner")
            .assign(bonus = lambda df: df.apply(_calculate_bonus, axis=1))
            .assign(total_bonus = lambda df: df["bonus"].sum())
            .filter(["total_salary", "total_bonus"])
            .drop_duplicates()
            .reset_index()
    )
    return


@app.cell
def _(department_df, employee_df):
    """
    Returns all deptno and dname from department along with the names of all the employees in
    each department (if there is an employee in a particular department):
    """

    (
        department_df
            .merge(employee_df, left_on="deptno", right_on="deptno", how="left")
            .filter(["deptno", "dname", "ename"])
            .reset_index()

    )
    return


@app.cell
def _(department_df, employee_df):
    """
    Returns all departments (deptno, dname) and all employees (ename) from the respective tables
    regardless of whether a department has an employee or an employee is assigned to a department
    """

    (
        employee_df
            .merge(department_df, left_on="deptno", right_on="deptno", how="outer")
            .filter(["deptno", "dname", "ename"])
            .reset_index()
    )
    return


@app.cell
def _(employee_df):
    """
    Find all employees in EMP whose commission (COMM) is less
    than the commission of employee WARD. Employees with a NULL commission
    should be included as well.

    Note: when using .loc on chained operation you'll have to use lamda function else the column for example: comm with fillna is not accessable
    """

    # _ward_commission = employee_df.loc[(employee_df["ename"] == "WARD"), "comm"].iloc[0]

    # (
    #     employee_df
    #         .as∏sign(comm = lambda df: df["comm"].fillna(0))
    #         .pipe(lambda df: df[df["comm"] < _ward_commission])
    # )

    _ward_commission = (
        next(iter(employee_df.loc[employee_df["ename"] == "WARD", "comm"]), 0)
    )

    (
        employee_df
            .assign(comm = lambda df: df["comm"].fillna(0))
            .loc[lambda df: df["comm"] < _ward_commission]
    )
    return


@app.cell
def _(employee_df):
    """
    Extract employee WARD commission to all rows
    Make sure to implement the solution in one liner

    - Solution with iloc will fail if the boolean mask used for results in empty result. 
    - You cannot use iloc in empty result

    - Solution with next(iter) is best becuase it provides a fallback value 0 if the result is empty

    Note:
    loc[boolean_mask, "column_name"] returns a series of values from colum_name
    loc[boolean_mask, ["column_name1", "column_name2"]] returns a dataframe with 2 columns
    """

    # (
    #     employee_df
    #         .assign(ward_commission = lambda df: (
    #             df.loc[df["ename"] == "WARD", "comm"].iloc[0]
    #         ))
    # )

    (
        employee_df
            .assign(ward_commission = lambda df: (
                next(iter(df.loc[df["ename"] == "WARD", "comm"]), 0)
            ))
    )



    return


@app.cell
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
