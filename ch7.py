import marimo

__generated_with = "0.19.9"
app = marimo.App()


@app.cell
def _():
    from typing import cast 

    import pandas as pd
    import numpy as np

    from data.employee import employee_df
    from data.employee_bonus import employee_bonus_df
    from data.new_salary import new_salary_df
    from data.department import department_df
    from data.department_accident import department_accident_df
    from data.sales import sales_df
    from data.transaction import transaction_df

    return cast, employee_df, np, pd, sales_df, transaction_df


@app.cell
def _(employee_df):
    """
    find the average salary for all employees
    """

    _employee_df = employee_df.copy()

    """
    Method one (preferred when only avg_sal is required)
    """

    # avg_salary = _employee_df["sal"].mean()

    # print(avg_salary)

    """
    Method two (preferred when multiple aggregates are required)

    Returns a dataframe
    where average_sal becomes the index of dataframe and sal becomes the column

    """

    _df = _employee_df.agg(
        average_sal=("sal", "mean"),
        total_sal=("sal", "sum")
    )

    print(_df["sal"]["average_sal"])
    print(_df["sal"]["total_sal"])
    return


@app.cell
def _(employee_df):
    """
    you want to find the highest and lowest salaries for all employees
    """

    _employee_df = employee_df.copy()

    _agg = _employee_df.agg(
        highest_sal = ("sal", "max"),
        lowest_sal = ("sal", "min")
    )

    print(_agg["sal"]["highest_sal"])
    print(_agg["sal"]["lowest_sal"])
    return


@app.cell
def _(employee_df):
    """
    find the average salary for each department
    deptno used in groupby becomes the index
    """

    _employee_df = employee_df.copy()

    _df = _employee_df.groupby("deptno").agg(
        average_sal = ("sal", "mean")
    )

    # print(_df["average_sal"][10])
    # print(_df["average_sal"][20])

    print(_df["average_sal"].to_dict())
    return


@app.cell
def _(employee_df):
    """
    you want to find the highest and lowest salaries for each department.
    """

    _employee_df = employee_df.copy()

    _agg = _employee_df.groupby("deptno").agg(
        dept_highest_sal = ("sal", "max"),
        dept_lowest_sal = ("sal", "min")
    )

    print(_agg["dept_highest_sal"].to_dict())
    print(_agg["dept_lowest_sal"].to_dict())
    return


@app.cell
def _(employee_df):
    """
    find the average salary for each department (PART TWO) 
    with as_index=False
    if you don't want deptno when using grouped by be part of index use as_index=Fase
    """

    _employee_df = employee_df.copy()

    _df = _employee_df.groupby("deptno", as_index=False).agg(
        average_sal = ("sal", "mean")
    )

    print(_df.to_dict(orient="records"))
    return


@app.cell
def _(employee_df):
    """
    You want to compute the sum of all values, such as all employee salaries, in a column.
    """

    _employee_df = employee_df.copy()

    _all_employee_sal = _employee_df["sal"].sum()

    print(_all_employee_sal)
    return


@app.cell
def _(employee_df):
    """
    You want to compute the sum of salaries for each department
    """

    _employee_df = employee_df.copy()

    _result = _employee_df.groupby("deptno").agg(
        total_sal = ("sal", "sum")
    )

    print(_result["total_sal"][10])
    return


@app.cell
def _(employee_df):
    """
    compute a running total of salaries for all employees

    select 
        ename,
        sal,
        sum(sal) over (order by sal, empno) as running_total
        from emp
    order by sal

    """

    _employee_df = employee_df.copy()

    _employee_df = _employee_df.sort_values(["sal", "empno"])
    _employee_df["running_total"] = _employee_df["sal"].expanding().sum()

    _result = _employee_df[["ename", "sal", "running_total"]].sort_values("sal")

    print(_result)
    return


@app.cell
def _():
    """
    7.7 Generating a Running Product
    """

    # TODO
    return


@app.cell
def _(cast, pd, sales_df):
    """
    You have a series of values that appear over time, such as monthly sales figures
    you want to implement a simple smoother, such as weighted running average to better identify the trend


    select 
        date1, 
        sales,
        lag(sales,1) over(order by date1) as salesLagOne,
        lag(sales,2) over(order by date1) as salesLagTwo,
        (sales + (lag(sales,1) over(order by date1)) + lag(sales,2) over(order by date1))/3 as MovingAverage
    from sales


    In pandas we have .rolling() method and there is no need to calculate lag 
    rolling(window=3).mean() does the job

    """


    """
    Method one
    """

    # _sales_df = sales_df.copy()

    # _sales_df = _sales_df.sort_values("date")

    # _sales_df["moving_average"] = _sales_df["sales"].rolling(window=3).mean()

    # _result_df = _sales_df[["date", "sales", "moving_average"]]

    # print(_result_df)


    """
    Method two (chained approach)
    """

    _sales_df = sales_df.copy().sort_values("date")

    _sales_df = (
        _sales_df
            .assign(
                moving_average = (
                    lambda df: cast(pd.DataFrame, df)["sales"].fillna(0).rolling(window=3).mean()
                ),
            )
    )

    _result_df = _sales_df[["date", "sales", "moving_average"]]

    print(_result_df)
    return


@app.cell
def _(sales_df):
    """
    A simple three-point weighted moving average that emphasizes the most
    recent data point could be implemented with the following variant on the solution,
    where coefficients and the denominator have been updated:

    select 
        date1,
        sales,lag(sales,1) over(order by date1),
        lag(sales,2) over(order by date1),
        ((3*sales) + (2*(lag(sales,1) over(order by date1))) + (lag(sales,2) over(order by date1)))/6 as sales_moving_average
    from sales
    """

    _sales_df = sales_df.copy().sort_values("date")

    _sales_df["sales_lag_one"] = _sales_df["sales"].shift(1)
    _sales_df["sales_lag_two"] = _sales_df["sales"].shift(2)

    _sales_df["sales_moving_average"] = (_sales_df["sales"] * 3) + (_sales_df["sales_lag_one"] * 2) + (_sales_df["sales_lag_two"] * 1) / 6

    print(_sales_df)
    return


@app.cell
def _(employee_df):
    """
    You want to find the mode (for those of you who don’t recall, the mode in mathemat‐
    ics is the element that appears most frequently for a given set of data) of the values in
    a column. For example, you want to find the mode of the salaries in DEPTNO 20.
    """

    _employee_df = employee_df.copy()

    dept_20_mode = _employee_df[_employee_df['deptno'] == 20]['sal'].mode().iloc[0]

    print(dept_20_mode)
    return


@app.cell
def _(employee_df):
    """
    you want to find the median of the salaries in deptno 20
    median and p50 is same thing

    select 
        percentile_disc(0.5) WITHIN GROUP (ORDER BY sal) AS discrete_median
    from emp
    where deptno = 20;

    where as in pandas you don't need to specify order by sal as it is smart enough to figure that out
    and do the order by itself internally when quanitle, median is used

    these type of functions are called: Ordered-Set Functions or Rank-Based Statistics or Ordered-Set Aggregates
    """

    """
    Method one
    """

    # _employee_df = employee_df.copy()

    # median_sal = _employee_df[_employee_df["deptno"] == 20]["sal"].median()

    # print(median_sal)

    """
    Method two
    """

    _employee_df = employee_df.copy()

    median_sal = _employee_df[_employee_df["deptno"] == 20]["sal"].quantile(0.5)

    print(median_sal)
    return


@app.cell
def _(employee_df):
    """
    you want to determine what percentage of all salaries are the salaries in DEPTNO 10 
    (the percentage that DEPTNO 10 salaries contribute to the total)

    select 
        (sum(case when deptno = 10 then sal end) / sum(sal)) * 100 as pct
    from emp

    """

    _employee_df = employee_df.copy()

    _result = (_employee_df.loc[_employee_df["deptno"] == 10, "sal"].sum() / _employee_df["sal"].sum()) * 100

    print(_result)
    return


@app.cell
def _(employee_df):
    """
    You want to perform an aggregation on a column, but the column is nullable. You
    want the accuracy of your aggregation to be preserved, but are concerned because
    aggregate functions ignore NULLs. For example, you want to determine the average
    commission for employees in DEPTNO 30, but there are some employees who do not
    earn a commission (COMM is NULL for those employees). Because NULLs are
    ignored by aggregates, the accuracy of the output is compromised. You would like to
    somehow include NULL values in your aggregation.
    """

    _employee_df = employee_df.copy()

    """
    Method one

    Pandas mean or any aggregate function ignores na value. 

    use:
    if you want to know: "Of the employee who actually have commission data, what is the average?
    """
    # _result = _employee_df.loc[_employee_df["deptno"] == 30]["comm"].mean()

    # print(_result)

    """
    Method two (preferred)

    fillna(0) to replace na values with 0

    use:
    What is the average commission cost per head for everyone in deptno 30?
    """

    _result = _employee_df.loc[_employee_df["deptno"] == 30]["comm"].fillna(0).mean()

    print(_result)

    return


@app.cell
def _(employee_df):
    """
    you want to compute the average salary of all employees
    excluding the highest and lowest salaries.

    In statistical language, this is known as a trimmed mean
    """

    _employee_df = employee_df.copy()

    min_sal = _employee_df["sal"].min()
    max_sal = _employee_df["sal"].max()

    _result = (
        _employee_df
            .loc[(_employee_df["sal"] > min_sal) & (_employee_df["sal"] < max_sal), "sal"]
            .mean()
    )

    print(_result)
    return


@app.cell
def _(np, pd, transaction_df):
    """
    A payment is “PY” and a purchase is “PR.” 
    If the value for TRX is PY, you want the current value for AMT subtracted from
    the running total
    If the value for TRX is PR, you want the current value for AMT added to the running total

    select 
        case when trx = 'PY' then 'PAYMENT' else 'PURCHASE' end trx_type,
        amount,
        sum(case when trx = 'PY' then -amount else amount end) over (order by id, amount) as balance
    from V

    """

    """
    Method one (using staging columns such as amount_signed)
    """

    # _transaction_df = transaction_df.copy()

    # def calculate_balance(df: pd.DataFrame):
    #     df["amount_signed"] = np.where(df["trx"] == "PR", df["amount"], -df["amount"])
    #     df["balance"] = df["amount_signed"].expanding().sum()

    #     return df.drop(columns=["amount_signed"])

    # _transaction_df = (
    #     _transaction_df
    #         .sort_values(["id", "amount"])
    #         .assign(trx_type = lambda df: np.where(df["trx"] == "PR", "Purchase", "Payment"))
    #         .pipe(calculate_balance)
    # )

    # print(_transaction_df)

    """
    Method two - without staging column in calculate balance

    creating a series from ndarray with index alignment with index=df.index
    """

    _transaction_df = transaction_df.copy()

    def calculate_balance(df: pd.DataFrame):
        amount_signed = pd.Series(
            np.where(df["trx"] == "PR", df["amount"], -df["amount"]),
            index=df.index
        )

        df["balance"] = amount_signed.expanding().sum()

        return df

    _transaction_df = (
        _transaction_df
            .sort_values(["id", "amount"])
            .assign(trx_type = lambda df: np.where(df["trx"] == "PR", "Purchase", "Payment"))
            .pipe(calculate_balance)
    )

    print(_transaction_df)
    return


@app.cell
def _(employee_df):
    """
    7.16 Finding Outliers Using the Median Absolute Deviation
    """

    _employee_df = employee_df.copy()

    median_sal = _employee_df["sal"].median()

    deviations = (_employee_df["sal"] - median_sal).abs()

    median_absolute_deviation = deviations.median()

    _employee_df["score"] = (_employee_df["sal"] - median_absolute_deviation) / median_absolute_deviation

    print(_employee_df.loc[:, ["empno", "ename", "sal", "score"]])
    return


@app.cell
def _():
    """
    7.17 Finding Anomalies Using Benford’s Law

    (IMPORTANT) -> TODO
    """
    return


if __name__ == "__main__":
    app.run()
