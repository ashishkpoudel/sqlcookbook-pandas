import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    from data.employee import employee_df
    from data.employee_bonus import employee_bonus_df
    from data.new_salary import new_salary_df
    from data.department import department_df
    from data.department_accident import department_accident_df
    return (
        department_accident_df,
        department_df,
        employee_bonus_df,
        employee_df,
        new_salary_df,
        pd,
    )


@app.cell
def _(employee_df):
    """
    Update the salary of employee in deptno 20 by 10%
    """

    """ Method one """
    # _employee_df = employee_df.copy()
    # _employee_df_mask = employee_df["deptno"] == 20
    # _employee_df.loc[_employee_df_mask, "sal"] = _employee_df.loc[_employee_df_mask, "sal"] * 1.10
    # _employee_df

    """ Method two """
    # def _increase_sal_by_10_per(sal):
    #     return sal * 1.10

    # _employee_df = employee_df.copy()
    # _employee_df_mask = _employee_df["deptno"] == 20
    # _employee_df.loc[_employee_df_mask, "sal"] = _employee_df.loc[_employee_df_mask, "sal"].apply(_increase_sal_by_10_per)
    # _employee_df


    """ Method three """
    _employee_df = employee_df.copy()
    _employee_df_mask = _employee_df["deptno"] == 20

    _employee_df.loc[_employee_df_mask, "sal"] = (
        _employee_df.loc[_employee_df_mask, "sal"] * 1.10
    ).round()

    _employee_df[["empno", "sal", "deptno"]]
    return


@app.cell
def _(employee_bonus_df, employee_df):
    """
    Update the salary of employee by 20% if their record exists in employee_bonus
    Note: Use apply function for any transformation logic

    _employee_df.loc[_bonus_mask, "sal"] = _employee_df.loc[_bonus_mask, "sal"].apply(
        lambda sal: round(sal * 1.10)
    )
    """

    _employee_df = employee_df.copy()
    _employee_bonus_df = employee_bonus_df.copy()

    _is_bonus_eligible = _employee_df["empno"].isin(_employee_bonus_df["empno"])
    _employee_df.loc[_is_bonus_eligible, "sal"] *= 1.20
    _employee_df.loc[_is_bonus_eligible]
    return


@app.cell
def _(employee_df, new_salary_df):
    """
    You want to update rows in one table using values from another. For example, you
    have a table called NEW_SAL, which holds the new salaries for certain employees.
    """

    dept_sal_map = (
        new_salary_df
            .drop_duplicates("deptno", keep="last")
            .set_index("deptno")["sal"]
    )

    _employee_df = employee_df.copy()
    _employee_df["sal"] = _employee_df["deptno"].map(dept_sal_map).fillna(_employee_df["sal"])

    _employee_df[["empno", "ename", "deptno", "sal"]]
    return


@app.cell
def _(employee_bonus_df, employee_df, pd):
    """
    • If any employee in EMP_COMMISSION also exists in table EMP, then update
    their commission (COMM) to 1000.
    • For all employees who will potentially have their COMM updated to 1000, if their
    SAL is less than 2000, delete them (they should not be exist in EMP_[.keep-
    together] COMMISSION).
    • Otherwise, insert the EMPNO, ENAME, and DEPTNO values from table EMP
    into table EMP_COMMISSION.
    """

    employee_commission = 1000
    salary_threshold = 2000

    _employee_df = employee_df.copy()
    _employee_bonus_df = employee_bonus_df.copy()

    exists_in_commission = _employee_df["empno"].isin(_employee_bonus_df["empno"])
    _employee_df.loc[exists_in_commission, "comm"] = employee_commission

    should_be_deleted = (exists_in_commission) & (_employee_df["sal"] < salary_threshold)

    _employee_df = _employee_df[~should_be_deleted]

    eligible_for_insert = exists_in_commission & (_employee_df["sal"] >= salary_threshold)

    new_commission_df = _employee_df.loc[
        eligible_for_insert,
        ["empno", "ename", "deptno"]
    ]

    _employee_bonus_df = pd.concat(
        [_employee_bonus_df, new_commission_df],
        ignore_index=True
    )

    print(_employee_bonus_df)
    return


@app.cell
def _(employee_df):
    """
    Delete from employee table where empno is 7782
    """
    employee_id = 7782

    """
    Method one (preferred)
    """

    # _employee_df = employee_df.copy()
    # _employee_df = _employee_df.query("empno != @employee_id")


    """
    Method two (preferred)
    """

    # _employee_df = employee_df.copy()
    # _employee_df = _employee_df[_employee_df["empno"] != employee_id]


    """
    Method three (is confusing with bitwise not operator)
    """

    _employee_df = employee_df.copy()
    _employee_df = _employee_df[~_employee_df["empno"].isin([employee_id])]

    print(_employee_df["empno"].tolist())
    return


@app.cell
def _(department_df, employee_df):
    """
    You want to delete records from a table when those records refer to nonexistent
    records in some other table. For example, some employees are assigned to depart‐
    ments that do not exist. You want to delete those employees.
    """

    _employee_df = employee_df.copy()
    employee_without_department = ~_employee_df["deptno"].isin(department_df["deptno"])

    _employee_df = _employee_df[~employee_without_department]

    print(_employee_df["empno"].tolist())

    return


@app.cell
def _(employee_bonus_df):
    """
    You want to delete duplicate records from a table
    """

    _employee_bonus_df = employee_bonus_df.copy()

    print(_employee_bonus_df["empno"].tolist())

    _employee_bonus_df = _employee_bonus_df.drop_duplicates("empno", keep="last")

    print(_employee_bonus_df["empno"].tolist())
    return


@app.cell
def _(department_accident_df, employee_df):
    """
    You want to delete from EMP the records for those employees working at a depart‐
    ment that has three or more accidents.
    """

    _employee_df = employee_df.copy()


    """
    Method one premitive
    """

    # dep_count_series = department_accident_df.groupby("deptno")["deptno"].count()
    # deptno = dep_count_series.loc[lambda count: count >= 3].index.tolist()

    # _employee_df = _employee_df[~_employee_df["deptno"].isin(deptno)]

    # print(_employee_df["empno"].tolist())


    """
    Method two clean approach
    """

    # deptno_with_accidents = (
    #     department_accident_df
    #         .groupby("deptno")["deptno"]
    #         .count()
    #         .loc[lambda count: count >= 3]
    #         .index
    #         .tolist()
    # )

    # _employee_df = _employee_df[~_employee_df["deptno"].isin(deptno_with_accidents)]

    # print(_employee_df["empno"].tolist())

    """
    Method three clean approach (preferred)
    """

    deptno_with_accidents = (
        department_accident_df
            .groupby("deptno")["deptno"]
            .count()
            .loc[lambda count: count >= 3]
            .index
            .tolist()
    )

    _employee_df = _employee_df.loc[
        lambda df: ~df["deptno"].isin(deptno_with_accidents)
    ]

    print(_employee_df["empno"].tolist())


    return


if __name__ == "__main__":
    app.run()
