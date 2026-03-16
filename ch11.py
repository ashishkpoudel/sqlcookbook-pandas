import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import pandas as pd

    from data.employee import employee_df
    from data.department import department_df

    return department_df, employee_df, pd


@app.cell
def _(employee_df, pd):
    """
    You want to paginate or “scroll through” a result set. For example, you want to return
    the first five salaries from table EMP, then the next five, and so forth. Your goal is to
    allow a user to view five records at a time

    ---

    How to rank the group of records that have the same value (i.e. ties):

    average: average rank of the group
    min: lowest rank in the group
    max: highest rank in the group
    first: ranks assigned in order they appear in the array
    dense: like ‘min’, but rank always increases by 1 between groups.
    """


    _employee_df = employee_df.copy()

    _employee_df["row_number"] = (
        _employee_df
            .sort_values("sal")
            ["sal"]
            .rank(method="first")
            .astype(pd.Int64Dtype())
    )

    _employee_df[_employee_df["row_number"].between(1,5)].sort_values("row_number")
    return


@app.cell
def _(employee_df, pd):
    """
    You want a query to return every other employee in table EMP; you want the first
    employee, third employee, and so forth
    """

    _employee_df = employee_df.copy()

    _employee_df["row_number"] = _employee_df.sort_values("ename")["ename"].rank(method="first").astype(pd.Int64Dtype())
    _employee_df.loc[_employee_df["row_number"] % 2 == 1, ["row_number", "ename", "sal"]]

    return


@app.cell
def _(pd):
    """"
    Example of row_numer, rank and dense_rank in pandas

    rank and dense_rank are value-based, not position-based.
    rank(method="min") and rank(method="dense") look at the sorted order of unique values internally.
    they assign the same rank to equal values regardless of original row order.
    So pre-sorting the DataFrame does not change those rank numbers.

    Pre-sort matters for row_number (or rank(method="first")) because ties are broken by row order, so ordering affects results.
    """

    _df = pd.DataFrame({
        "name": ["binay", "harish", "ashish", "ramesh","ashish", "binay"]
    })

    _df["row_number"] = _df.sort_values("name")["name"].rank(method="first")

    _df["rank"] = _df["name"].rank(method="min")
    _df["dense_rank"] = _df["name"].rank(method="dense")

    _df
    return


@app.cell
def _(department_df, employee_df):
    """
    You want to return the name and department information for all employees in
    departments 10 and 20 along with department information for departments 30 and
    40 (but no employee information).
    """

    _employee_df = employee_df.copy()
    _department_df = department_df.copy()

    _department_df = _department_df[_department_df["deptno"].isin([10,20,30,40])]
    _employee_df = _employee_df[_employee_df["deptno"].isin([10, 20])]

    _result_df = (
        _department_df[["deptno", "dname"]]
            .merge(_employee_df[["ename", "deptno"]], how="left", on="deptno")
            .sort_values(["deptno", "ename"], na_position="last")
            .reset_index(drop=True)
    )

    _result_df
    return


@app.cell
def _(pd):
    """
    You have a table containing the results of two tests, and you want to determine which
    pair of scores are reciprocals
    """

    _df = pd.DataFrame({
        'test1': [20, 50, 20, 60, 70, 80, 90, 100, 110, 120, 130, 140],
        'test2': [20, 25, 20, 30, 90, 130, 70, 50, 55, 60, 80, 70]
    })

    _reciprocals = (
        _df.merge(
            _df,
            left_on=["test1", "test2"],
            right_on=["test2", "test1"],
            suffixes=("_v1", "_v2")
        )
    )[["test1_v1", "test2_v2"]]

    _reciprocals.drop_duplicates()
    return


@app.cell
def _(employee_df):
    """
    You want to limit a result set to a specific number of records based on a ranking of
    some sort. For example, you want to return the names and salaries of the employees
    with the top five salaries
    """

    _employee_df = employee_df.copy()

    _employee_df["sal_dense_rank"] = _employee_df["sal"].rank(method="dense")

    _employee_df.loc[_employee_df["sal_dense_rank"] <= 5, ["empno", "ename", "sal", "sal_dense_rank"]]
    return


@app.cell
def _(employee_df):
    """
    You want to find “extreme” values in your table. For example, you want to find the
    employees with the highest and lowest salaries in table EMP.
    """

    _employee_df = employee_df.copy()

    min_sal = _employee_df["sal"].min()
    max_sal = _employee_df["sal"].max()

    _employee_df.loc[_employee_df["sal"].isin([min_sal, max_sal]), ["empno", "ename", "sal"]]
    return


@app.cell
def _(employee_df):
    """
    You want to find any employees who earn less than the employee hired immediately
    after them. Based on the following result set:
    """

    _employee_df = employee_df.copy()

    # salary of employee hired immediately after them
    _employee_df["sal_next"] = _employee_df.sort_values("hiredate")["sal"].shift(-1) 

    _employee_df.loc[_employee_df["sal"] < _employee_df["sal_next"], ["empno", "ename", "hiredate", "sal", "sal_next"]]
    return


@app.cell
def _(employee_df):
    """
    You want to return each employee’s name and salary along with the next highest and
    lowest salaries. If there are no higher or lower salaries, you want the results to wrap
    (first SAL shows last SAL and vice versa).
    """
    _employee_df = employee_df.copy()

    min_sal = _employee_df["sal"].min()
    max_sal = _employee_df["sal"].max()

    # lead over
    _employee_df["highest_sal"] = _employee_df.sort_values("sal")["sal"].shift(-1).fillna(min_sal)

    # lag over
    _employee_df["lowest_sal"] = _employee_df.sort_values("sal")["sal"].shift(1).fillna(max_sal)

    _employee_df.loc[:, ["empno", "ename", "sal", "highest_sal", "lowest_sal"]].sort_values("sal")
    return


@app.cell
def _(employee_df):
    """
    You want to rank the salaries in table EMP while allowing for ties
    """

    _employee_df = employee_df.copy()

    # dense_rank() over(order by sal)

    _employee_df["rank"] = employee_df.sort_values("sal")["sal"].rank(method="dense")

    _employee_df.loc[:, ["empno", "ename", "rank", "sal"]].sort_values("rank")
    return


@app.cell
def _(employee_df):
    """
    You want to find the different job types in table EMP but do not want to see dupli‐
    cates
    """

    _employee_df = employee_df.copy()

    _employee_df.drop_duplicates(subset=["job"])["job"]
    return


@app.cell
def _(employee_df):
    """
    You want return a result set that contains each employee’s name, the department they
    work in, their salary, the date they were hired, and the salary of the last employee
    hired, in each department.
    """

    _employee_df = employee_df.copy()

    _employee_df["max_sal_in_dept"] = _employee_df.groupby("deptno")["sal"].transform('max')

    _employee_df.loc[:, ["empno", "ename", "sal", "deptno", "max_sal_in_dept"]]

    return


@app.cell
def _(pd):
    """ 
    TODO

    11.12 Generating Simple Forecasts

    Based on current data, you want to return additional rows and columns representing
    future actions. For example, consider the following result set:

    ID ORDER_DATE PROCESS_DATE
    -- ----------- ------------
    1 25-SEP-2005 27-SEP-2005
    2 26-SEP-2005 28-SEP-2005
    3 27-SEP-2005 29-SEP-2005

    You want to return three rows per row returned in your result set (each row plus two
    additional rows for each order). Along with the extra rows, you would like to return
    two additional columns providing dates for expected order processing.
    From the previous result set, you can see that an order takes two days to process. For
    the purposes of this example, let’s say the next step after processing is verification,
    and the last step is shipment. Verification occurs one day after processing, and ship‐
    ment occurs one day after verification. You want to return a result set expressing the
    whole procedure. Ultimately you want to transform the previous result set to the fol‐
    lowing result set:

    ID ORDER_DATE PROCESS_DATE VERIFIED SHIPPED
    -- ----------- ------------ ----------- -----------
    1 25-SEP-2005 27-SEP-2005
    1 25-SEP-2005 27-SEP-2005 28-SEP-2005
    1 25-SEP-2005 27-SEP-2005 28-SEP-2005 29-SEP-2005
    2 26-SEP-2005 28-SEP-2005
    2 26-SEP-2005 28-SEP-2005 29-SEP-2005
    2 26-SEP-2005 28-SEP-2005 29-SEP-2005 30-SEP-2005
    3 27-SEP-2005 29-SEP-2005
    3 27-SEP-2005 29-SEP-2005 30-SEP-2005
    3 27-SEP-2005 29-SEP-2005 30-SEP-2005 01-OCT-2005
    """

    _df = pd.DataFrame({
        'id': [1, 2, 3],
        'order_date': ['25-SEP-2005', '26-SEP-2005', '27-SEP-2005'],
        'process_date': ['27-SEP-2005', '28-SEP-2005', '29-SEP-2005']
    })

    _df["id"].astype(pd.Int64Dtype())
    _df["order_date"].astype("datetime64[ns]")
    _df["process_date"].astype("datetime64[ns]")


    return


if __name__ == "__main__":
    app.run()
