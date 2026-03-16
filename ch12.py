# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.20.2",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import numpy as np

    from data.employee import employee_df
    from data.transaction_full import transaction_df

    return employee_df, np, pd, transaction_df


@app.cell
def _(employee_df, pd):
    """
    You want to take values from groups of rows and turn those values into columns in a
    single row per group. For example, you have a result set displaying the number of
    employees in each department:
    DEPTNO CNT
    ------ ----------
    10 3
    20 5
    30 6
    You would like to reformat the output so that the result set looks as follows:
    DEPTNO_10 DEPTNO_20 DEPTNO_30
    --------- ---------- ----------
    3 5 6
    """

    _employee_df = employee_df.copy()

    _result_df = pd.DataFrame([{
        "deptno_10": (_employee_df["deptno"] == 10).sum(),
        "deptno_20": (_employee_df["deptno"] == 20).sum(),
        "deptno_30": (_employee_df["deptno"] == 30).sum(),
    }])

    _result_df
    return


@app.cell
def _(employee_df):
    """
    For every unique department in employee df create a column eg: dep_10 with the count of employees
    """

    _employee_df = employee_df.copy()

    _employee_per_department = (
        _employee_df
            .groupby("deptno")
            .size()
            .to_frame(name="count")
            .reset_index()
    )

    _pivot = _employee_per_department.pivot_table(
        columns="deptno",
        values="count"
    )

    _pivot.columns = [f"dept_{column}" for column in _pivot.columns]

    _pivot
    return


@app.cell
def _(employee_df):
    """
    12.2 Pivoting a Result Set into Multiple Rows

    You want to turn rows into columns by creating a column corresponding to each of
    the values in a single given column. However, unlike in the previous recipe, you need
    multiple rows of output. Like the earlier recipe, pivoting into multiple rows is a fun‐
    damental method of reshaping data.

    For example, you want to return each employee and their position (JOB), and you
    currently use a query that returns the following result set:

    You would like to format the result set such that each job gets its own column:

    TODO: when reading example always check what happens when you remove index="row_number"
    cumcount means cumulative count (running count within each group).
    """

    _employee_df = employee_df.copy()[["ename", "job"]]
    _employee_df["row_number"] = _employee_df.groupby("job").cumcount()

    _pivot_df = _employee_df.pivot(
        index="row_number",
        columns="job",
        values="ename",
    ).reset_index(drop=True)

    _pivot_df
    return


@app.cell
def _(pd):
    """
    You want to transform columns to rows. Consider the following result set:
    deptno_10 deptno_20 deptno_30
    ---------- ---------- ----------
    3 5 6
    You would like to convert that to the following:
    deptno count
    ------ --------------
    10 3
    20 5
    30 6
    """

    _df = pd.DataFrame({
        "deptno_10": [3],
        "deptno_20": [5],
        "deptno_30": [6]
    })


    _df_long = _df.melt(
        id_vars=None,
        var_name="deptno",
        value_name="count"
    )

    _df_long["deptno"] = _df_long["deptno"].str.replace("deptno_", "").astype(pd.Int64Dtype())

    _df_long
    return


@app.cell
def _(employee_df, pd):
    """
    You want to return all columns from a query as just one column. For example, you
    want to return the ENAME, JOB, and SAL of all employees in DEPTNO 10, and you
    want to return all three values in one column. You want to return three rows for each
    employee and one row of white space between employees. You want to return the fol‐
    lowing result set:
    EMPS
    ----------
    CLARK
    MANAGER
    2450
    KING
    PRESIDENT
    5000
    MILLER
    CLERK
    1300
    """

    _employee_df = employee_df.copy()

    _employee_df = _employee_df.loc[
        _employee_df["deptno"].isin([10]),
        ["ename", "job", "sal", "deptno"]
    ]

    _employee_df["_blank"] = "--"

     # verticalize columns into one Series using stack
     # drop last blank line using iloc[:-1]
     # figure out: somehow i was not able to call to_frame after reset_index() which is why the result is wrapped in pd.Series

    _result_df = pd.Series(_employee_df.stack().reset_index(drop=True)).iloc[:-1].to_frame("emps")

    _result_df
    return


@app.cell
def _(employee_df, pd):
    """
    You are generating a report, and when two rows have the same value in a column,
    you want to display that value only once. For example, you want to return DEPTNO
    and ENAME from table EMP, you want to group all rows for each DEPTNO, and you
    want to display each DEPTNO only one time. You want to return the following result
    set:

    DEPTNO ENAME
    ------ ---------
    10  CLARK
        KING
        MILLER

    20  SMITH
        ADAMS
        FORD
        SCOTT
        JONES

    30  ALLEN
        BLAKE
        MARTIN
        JAMES
        TURNER
        WARD
    """

    _employee_df = employee_df.copy()

    _employee_df = _employee_df[["deptno", "ename"]].sort_values(["deptno", "ename"])

    _employee_df["deptno"] = (
        _employee_df["deptno"]
            .mask(_employee_df["deptno"].duplicated(), pd.NA)
    )

    _employee_df
    return


@app.cell
def _(employee_df, pd):
    """
    12.6 Pivoting a Result Set to Facilitate Inter-Row Calculations

    You want to make calculations involving data from multiple rows. To make your job
    easier, you want to pivot those rows into columns such that all values you need are
    then in a single row.

    You want to calculate the difference between the salaries of DEPTNO 20 and
    DEPTNO 10 and between DEPTNO 20 and DEPTNO 30.
    The final result will look like this:
    d20_10_diff d20_30_diff
    ------------ ----------
    2125 1475
    """

    _employee_df = employee_df.copy()

    _dep_salary_lookup = (
        _employee_df.groupby("deptno")["sal"].sum()
    )

    _result_df = pd.DataFrame({
        "d20_10_diff": [_dep_salary_lookup[20] - _dep_salary_lookup[10]],
        "d20_30_diff": [_dep_salary_lookup[20] - _dep_salary_lookup[30]]
    })

    _result_df
    return


@app.cell
def _(employee_df, np):
    """
    12.7 Creating Buckets of Data, of a Fixed Size

    You want to organize data into evenly sized buckets, with a predetermined number of
    elements in each bucket. The total number of buckets may be unknown, but you want
    to ensure that each bucket has five elements. For example, you want to organize the
    employees in table EMP into groups of five based on the value of EMPNO, as shown
    in the following results:

    GRP EMPNO ENAME
    --- ---------- -------
    1 7369 SMITH
    1 7499 ALLEN
    1 7521 WARD
    1 7566 JONES
    1 7654 MARTIN
    2 7698 BLAKE
    2 7782 CLARK
    2 7788 SCOTT
    2 7839 KING
    2 7844 TURNER
    3 7876 ADAMS
    3 7900 JAMES
    3 7902 FORD
    3 7934 MILLER


    The solution to this problem is greatly simplified by functions for ranking rows. Once
    the rows are ranked, creating buckets of five is simply a matter of dividing and then
    taking the mathematical ceiling of the quotient.
    Use the window function ROW_NUMBER OVER to rank each employee by
    EMPNO. Then divide by five to create the groups 

    """

    _employee_df = employee_df.copy()[["empno", "ename"]].sort_values(["empno", "ename"])

    _employee_df["row_number"] = np.ceil(_employee_df["empno"].rank(method="first") / 5.0)

    _employee_df
    return


@app.cell
def _(employee_df, np, pd):
    """
    12.8 Creating a Predefined Number of Buckets

    You want to organize your data into a fixed number of buckets. For example, you
    want to organize the employees in table EMP into four buckets.

    The solution to this problem is simple now that the NTILE function is widely avail‐
    able. NTILE organizes an ordered set into the number of buckets you specify, with
    any stragglers distributed into the available buckets starting from the first bucket. The
    desired result set for this recipe reflects this: buckets 1 and 2 have four rows, while
    buckets 3 and 4 have three rows.

    """

    _employee_df = employee_df.copy()[["empno", "ename"]].sort_values("empno")

    # buckets starts with 0 so we are adding 1 so that bucket becomes 1, 2, 3, 4
    _employee_df["bucket"] = pd.qcut(_employee_df["empno"], q=4, labels=False) + 1

    # This replicates NTILE exactly by using the row position
    _employee_df['bucket_manual'] = np.ceil(_employee_df["empno"].rank(method='first') / (len(_employee_df) / 4)).astype(int)

    _employee_df


    return


@app.cell
def _(employee_df):
    """
    12.9 Creating Horizontal Histograms

    You want to use SQL to generate histograms that extend horizontally. For example,
    you want to display the number of employees in each department as a horizontal his‐
    togram with each employee represented by an instance of *. You want to return the
    following result set:
    DEPTNO CNT
    ------ ----------
    10 ***
    20 *****
    30 ******
    """

    _employee_df = employee_df.copy()

    _dep_employee_count = _employee_df.groupby("deptno").size().to_frame("count")
    _dep_employee_count["count"] = _dep_employee_count["count"].apply(lambda count: "*" * count)

    _dep_employee_count
    return


@app.cell
def _():
    """
    2.10 Creating Vertical Histograms

    You want to generate a histogram that grows from the bottom up. For example, you
    want to display the number of employees in each department as a vertical histogram
    with each employee represented by an instance of *. You want to return the following
    result set:

    TODO

    D10 D20 D30
    --- --- ---
    *
    * *
    * *
    * * *
    * * *
    * * *
    """



    return


@app.cell
def _(employee_df, pd):
    """
    12.11 Returning Non-GROUP BY Columns

    Problem
    You are executing a GROUP BY query, and you want to return columns in your select
    list that are not also listed in your GROUP BY clause. This is not normally possible,
    as such ungrouped columns would not represent a single value per row.
    Say that you want to find the employees who earn the highest and lowest salaries in
    each department, as well as the employees who earn the highest and lowest salaries in
    each job. You want to see each employee’s name, the department he works in, his job
    title, and his salary. You want to return the following result set:
    DEPTNO ENAME JOB SAL DEPT_STATUS JOB_STATUS
    ------ ------ --------- ----- --------------- --------------
    10 MILLER CLERK 1300 LOW SAL IN DEPT TOP SAL IN JOB
    10 CLARK MANAGER 2450 LOW SAL IN JOB
    10 KING PRESIDENT 5000 TOP SAL IN DEPT TOP SAL IN JOB
    20 SCOTT ANALYST 3000 TOP SAL IN DEPT TOP SAL IN JOB
    20 FORD ANALYST 3000 TOP SAL IN DEPT TOP SAL IN JOB
    20 SMITH CLERK 800 LOW SAL IN DEPT LOW SAL IN JOB
    20 JONES MANAGER 2975 TOP SAL IN JOB
    30 JAMES CLERK 950 LOW SAL IN DEPT
    30 MARTIN SALESMAN 1250 30 WARD SALESMAN 1250 30 ALLEN SALESMAN 1600 LOW SAL IN JOB
    LOW SAL IN JOB
    TOP SAL IN JOB
    30 BLAKE MANAGER 2850 TOP SAL IN DEPT
    """

    _employee_df = employee_df.copy()[["ename", "deptno", "sal", "job"]]

    _employee_df["max_department_sal"] = _employee_df.groupby("deptno")["sal"].transform("max")
    _employee_df["min_department_sal"] = _employee_df.groupby("deptno")["sal"].transform("min")
    _employee_df["max_job_sal"] = _employee_df.groupby("job")["sal"].transform("max")
    _employee_df["min_job_sal"] = _employee_df.groupby("job")["sal"].transform("min")

    def department_status(row: pd.Series):
        if row["sal"] == row["max_department_sal"]:
            return "top sal in department"
        elif row["sal"] == row["min_department_sal"]:
            return "low sal in department"

        return "-"

    def job_status(row: pd.Series):
        if row["sal"] == row["max_job_sal"]:
            return "top sal in job"
        elif row["sal"] == row["min_job_sal"]:
            return "low sal in job"

        return "-"

    _employee_df["department_sal_status"] = _employee_df.apply(department_status, axis=1)
    _employee_df["job_sal_status"] = _employee_df.apply(job_status, axis=1)

    _employee_df

    return


@app.cell
def _(employee_df):
    """
    2.12 Calculating Simple Subtotals
    Problem
    For the purposes of this recipe, a simple subtotal is defined as a result set that contains
    values from the aggregation of one column along with a grand total value for the
    table. An example would be a result set that sums the salaries in table EMP by JOB
    and that also includes the sum of all salaries in table EMP. The summed salaries by
    JOB are the subtotals, and the sum of all salaries in table EMP is the grand total. Such
    a result set should look as follows:
    JOB SAL
    --------- ----------
    ANALYST 6000
    CLERK 4150
    MANAGER 8275
    PRESIDENT 5000
    SALESMAN 5600
    TOTAL 29025
    """

    _employee_df = employee_df.copy()

    _pivot_df = _employee_df.pivot_table(
        index="job",
        values="sal",
        aggfunc="sum",
        margins=True,
        margins_name="TOTAL"
    ).reset_index()

    _pivot_df
    return


@app.cell
def _():
    """
    TODO

    12.13 Calculating Subtotals for All Possible Expression
    Combinations

    Problem
    You want to find the sum of all salaries by DEPTNO, and by JOB, for every JOB/
    DEPTNO combination. You also want a grand total for all salaries in table EMP. You
    want to return the following result set:

    DEPTNO JOB CATEGORY SAL
    ------ --------- --------------------- -------
    10 CLERK TOTAL BY DEPT AND JOB 1300
    10 MANAGER TOTAL BY DEPT AND JOB 2450
    10 PRESIDENT TOTAL BY DEPT AND JOB 5000
    20 CLERK TOTAL BY DEPT AND JOB 1900
    400 | Chapter 12: Reporting and Reshaping
    30 CLERK TOTAL BY DEPT AND JOB 950
    30 SALESMAN TOTAL BY DEPT AND JOB 5600
    30 MANAGER TOTAL BY DEPT AND JOB 2850
    20 MANAGER TOTAL BY DEPT AND JOB 2975
    20 ANALYST TOTAL BY DEPT AND JOB 6000
    CLERK TOTAL BY JOB 4150
    ANALYST TOTAL BY JOB 6000
    MANAGER TOTAL BY JOB 8275
    PRESIDENT TOTAL BY JOB 5000
    SALESMAN TOTAL BY JOB 5600
    10 TOTAL BY DEPT 8750
    30 TOTAL BY DEPT 9400
    20 TOTAL BY DEPT 10875
    GRAND TOTAL FOR TABLE 29025
    """
    return


@app.cell
def _():
    """
    TODO

    12.14 Identifying Rows That Are Not Subtotals
    """
    return


@app.cell
def _(employee_df, np):
    """
    12.15 Using Case Expressions to Flag Rows
    Problem
    You want to map the values in a column, perhaps the EMP table’s JOB column, into a
    series of “Boolean” flags. 
    """

    _employee_df = employee_df.copy()[["ename", "job"]]

    _employee_df["is_clerk"] = np.where(_employee_df["job"] == "CLERK", 1, 0)
    _employee_df["is_sales"] = np.where(_employee_df["job"] == "SALESMAN", 1, 0)
    _employee_df["is_manager"] = np.where(_employee_df["job"] == "MANAGER", 1, 0)
    _employee_df["is_analyst"] = np.where(_employee_df["job"] == "ANALYST", 1, 0)
    _employee_df["is_president"] = np.where(_employee_df["job"] == "PRESIDENT", 1, 0)

    _employee_df.sort_values(["is_clerk", "is_sales", "is_manager", "is_analyst", "is_president"])
    return


@app.cell
def _():
    """
    TODO

    12.16 Creating a Sparse Matrix
    """
    return


@app.cell
def _(pd, transaction_df):
    """
    REVIST - SOLUTION FROM LLM

    12.17 Grouping Rows by Units of Time

    Problem
    You want to summarize data by some interval of time. For example, you have a trans‐
    action log and want to summarize transactions by five-second intervals.
    """

    _transaction_df = transaction_df.copy()

    _transaction_df['trx_date'] = pd.to_datetime(
        _transaction_df["trx_date"], 
    )

    # using pd.Grouper to aggregate every 5 seconds
    # '5s' is the frequency alias for 5 seconds

    summary = (
        _transaction_df
            .groupby(pd.Grouper(key='trx_date', freq='5s'))['trx_count']
            .sum()
            .reset_index()
    )

    summary
    return


@app.cell
def _(employee_df):
    """
    12.18 Performing Aggregations over Different Groups/
    Partitions Simultaneously
    Problem
    You want to aggregate over different dimensions at the same time. For example, you
    want to return a result set that lists each employee’s name, their department, the num‐
    ber of employees in their department (themselves included), the number of employ‐
    ees that have the same job (themselves included in this count as well), and the total
    number of employees in the EMP table.
    """

    _employee_df = employee_df.copy()[["ename", "deptno", "job"]]
    _employee_df["emp_in_same_dept"] = _employee_df.groupby("deptno").transform("size")
    _employee_df["emp_in_same_job"] = _employee_df.groupby("job").transform("size")

    _employee_df
    return


@app.cell
def _(employee_df, pd):
    """
    12.19 Performing Aggregations over a Moving Range of Values

    Problem
    You want to compute a moving aggregation, such as a moving sum on the salaries in
    table EMP. You want to compute a sum for every 90 days, starting with the HIRE‐
    DATE of the first employee. You want to see how spending has fluctuated for every
    90-day period between the first and last employee hired. You want to return the fol‐
    lowing result set:

    HIREDATE SAL SPENDING_PATTERN
    ----------- ------- ----------------
    17-DEC-200 800 800
    20-FEB-2011 1600 2400
    22-FEB-2011 1250 3650
    02-APR-2011 2975 5825
    01-MAY-2011 2850 8675
    09-JUN-2011 2450 8275
    08-SEP-2011 1500 1500
    28-SEP-2011 1250 2750
    17-NOV-2011 5000 7750
    03-DEC-2011 950 11700
    03-DEC-2011 3000 11700
    23-JAN-2012 1300 10250
    09-DEC-2012 3000 3000
    12-JAN-2013 1100 4100
    """

    _employee_df = employee_df.copy()

    _employee_df["hiredate"] = pd.to_datetime(_employee_df["hiredate"])
    _employee_df = _employee_df.sort_values("hiredate")

    # 1. Calculate the raw rolling sum (Row-by-Row)
    _employee_df["rolling_raw"] = (
        _employee_df.rolling(window="90D", on="hiredate")["sal"].sum()
    )

    # 2. Fix the "Ties" (The SQL Range Logic)
    # This ensures that if 3 people are hired on the same day, they all show 
    # the final sum for that day.
    _employee_df["spending_pattern"] = (
        _employee_df.groupby("hiredate")["rolling_raw"].transform("max")
    )


    _employee_df[["ename", "sal", "rolling_raw", "spending_pattern"]]
    return


@app.cell
def _(employee_df):
    """
    TODO

    12.20 Pivoting a Result Set with Subtotals

    Problem
    You want to create a report containing subtotals and then transpose the results to
    provide a more readable report. For example, you’ve been asked to create a report
    that displays for each department, the managers in the department, and a sum of the
    salaries of the employees who work for those managers. Additionally, you want to
    return two subtotals: the sum of all salaries in each department for those employees
    who have managers, and a sum of all salaries in the result set (the sum of the depart‐
    ment subtotals).
    """

    _employee_df = employee_df.copy()

    return


if __name__ == "__main__":
    app.run()
