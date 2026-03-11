import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import pandas as pd

    from data.project import project_df
    from data.employee import employee_df

    return employee_df, pd, project_df


@app.cell
def _(project_df):
    """
    10.1 Locating a Range of Consecutive Values

    You want to determine which rows represent a range of consecutive projects
    """

    _project_df = project_df.copy()

    _project_df["next_start_date"] = (
        _project_df.sort_values("project_id")["start_date"].shift(-1)
    )

    _project_df[_project_df["end_date"] == _project_df["next_start_date"]]
    return


@app.cell
def _(employee_df):
    """
    You want to return the DEPTNO, ENAME, and SAL of each employee along with the
    difference in SAL between employees in the same department (i.e., having the same
    value for DEPTNO). The difference should be between each current employee and
    the employee hired immediately afterward (you want to see if there is a correlation
    between seniority and salary on a “per department” basis). For each employee hired
    last in his department, return “N/A” for the difference.
    """

    _employee_df = employee_df.copy()

    """
    Method one
    """
    # _employee_df["diff"] = (
    #     _employee_df
    #         .sort_values(["deptno", "hiredate"])
    #         .groupby("deptno")["sal"]
    #         .transform(lambda x: x - x.shift(-1))
    # )


    """
    Method two
    """
    _employee_df["next_sal"] = _employee_df.sort_values(["deptno", "hiredate"]).groupby("deptno")["sal"].shift(-1).fillna(0)
    _employee_df["diff"] = _employee_df["sal"] - _employee_df["next_sal"]


    _employee_df[["empno", "ename", "deptno", "sal", "diff"]]
    return


@app.cell
def _():

    """
    You want to return the DEPTNO, ENAME, and SAL of each employee along with the
    difference in SAL between employees in the same department (i.e., having the same
    value for DEPTNO). The difference should be between each current employee and
    the employee hired immediately afterward (you want to see if there is a correlation
    between seniority and salary on a “per department” basis). For each employee hired
    last in his department, return “N/A” for the difference.

    VERSION: 2 (TODO)

    - Current implementation computes next_sal using row-level shift(-1) after sorting.
    - This fails business logic when multiple hires exist on the same deptno + hiredate.

    Expected behavior:
    - For each deptno + hiredate, determine the latest hire and use that salary as the representative salary for that date.
    - For each row/date in a department, next_sal should come from the next hire date’s representative salary.
    - If no next hire date exists, next_sal = 0.
    - diff = sal - next_sal.

    Open design decision:
    - define explicit tie-breaker for “latest hire” on same date (e.g., max empno or max created_at).

    """
    return


@app.cell
def _():
    """
    10.3 Locating the Beginning and End of a Range of
    Consecutive Values

    TODO
    """
    return


@app.cell
def _(employee_df, pd):
    """
    You want to return the number of employees hired each year for the entire decade of
    the 2005s, but there are some years in which no employees were hired. 
    """
    from datetime import datetime, timedelta

    _employee_df = employee_df.copy()

    date_min = datetime.fromisoformat(_employee_df["hiredate"].min())
    date_max = datetime.fromisoformat(_employee_df["hiredate"].max())

    # expanding the range to test if missing values will apear in the final result with 0 count
    date_max = date_max + timedelta(days=365 * 3)

    year_range = pd.period_range(date_min, date_max, freq="Y").year.to_list()

    year_range_df = pd.DataFrame({
        "year": year_range
    })

    _employee_df["hiredate_year_only"] = _employee_df["hiredate"].astype("datetime64[ns]").dt.year

    hired_per_year = (
        _employee_df.groupby("hiredate_year_only", as_index=False)
        .size()
        .rename(columns={ "size": "count" })
    )

    _res = (
        year_range_df
            .merge(hired_per_year, how="left", left_on="year", right_on="hiredate_year_only")
            .fillna({ "count": 0 })
            [["year", "count"]]
    )

    _res
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
