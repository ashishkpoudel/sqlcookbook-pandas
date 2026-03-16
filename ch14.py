import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import pandas as pd

    from data.employee import employee_df

    return employee_df, pd


@app.cell
def _(employee_df):
    """
    14.1 Creating Cross-Tab Reports Using SQL Server’s PIVOT
    Operator
    Problem
    You want to create a cross-tab report to transform your result set’s rows into columns.
    You are aware of traditional methods of pivoting but would like to try something dif‐
    ferent. In particular, you want to return the following result set without using CASE
    expressions or joins:
    DEPT_10 DEPT_20 DEPT_30 DEPT_40
    ------- ----------- ----------- ----------
    3 5 6 0
    """

    _employee_df = employee_df.copy()

    _employee_df = (
        employee_df
            .groupby("deptno")["deptno"]
            .size()
            .to_frame("count")
            .reset_index()
    )

    # count col becomes the index - reset_index(drop=True) drops it
    # use reset_index without drop = True to preserve the count value

    _pivot_df = _employee_df.pivot_table(
        columns="deptno",
        values="count"
    ).reset_index(drop=True)

    _pivot_df
    return


@app.cell
def _(pd):
    """
    14.2 Unpivoting a Cross-Tab Report Using SQL Server’s
    UNPIVOT Operator
    Problem
    You have a pivoted result set (or simply a fact table), and you want to unpivot the
    result set. For example, instead of having a result set with one row and four columns,
    you want to return a result set with two columns and four rows. Using the result set
    from the previous recipe, you want to convert it from this:

    ACCOUNTING RESEARCH SALES OPERATIONS
    ---------- ---------- ---------- ----------
    3 5 6 0
    """

    _pivot_df = pd.DataFrame({
        "Accounting": [3],
        "Research": [2],
        "Sales": [10], 
        "Operations": [5]
    })

    _melt_df = _pivot_df.melt(
        id_vars=None,
        var_name="dname",
        value_name="count"
    )

    _melt_df
    return


@app.cell
def _():
    """
    14.4 Extracting Elements of a String from Unfixed
    Locations
    Problem
    You have a string field that contains serialized log data. You want to parse through the
    string and extract the relevant information. Unfortunately, the relevant information is
    not at fixed points in the string. Instead, you must use the fact that certain characters
    exist around the information you need, to extract said information.
    """
    return


@app.cell
def _():
    """
    14.8 Pivoting a Ranked Result Set
    Problem
    You want to rank the values in a table and then pivot the result set into three col‐
    umns. The idea is to show the top three, the next three, and then all the rest. For
    example, you want to rank the employees in table EMP by SAL and then pivot the
    results into three columns.
    """
    return


@app.cell
def _():
    """
    14.13 Testing for Existence of a Value Within a Group
    Problem
    You want to create a Boolean flag for a row depending on whether any row in its
    group contains a specific value. Consider an example of a student who has taken a
    certain number of exams during a period of time. A student will take three exams
    over three months. If a student passes one of these exams, the requirement is satisfied
    and a flag should be returned to express that fact. If a student did not pass any of the
    three tests in the three-month period, then an additional flag should be returned to
    express that fact as well. 
    """
    return


if __name__ == "__main__":
    app.run()
