import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    """
    13.1 Expressing a Parent-Child Relationship
    Problem
    You want to include parent information along with data from child records. For
    example, you want to display each employee’s name along with the name of their
    manager. You want to return the following result set:
    EMPS_AND_MGRS
    ------------------------------
    FORD works for JONES
    SCOTT works for JONES
    JAMES works for BLAKE
    TURNER works for BLAKE
    MARTIN works for BLAKE
    WARD works for BLAKE
    ALLEN works for BLAKE
    MILLER works for CLARK
    ADAMS works for SCOTT
    CLARK works for KING
    BLAKE works for KING
    JONES works for KING
    SMITH works for FORD
    """
    return


if __name__ == "__main__":
    app.run()
