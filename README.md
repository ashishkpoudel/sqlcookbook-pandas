## Pandas method chaining techniques
https://github.com/danieleongari/pandas-chaining-ninja

## Terminology
- Series: 
    Vector → 1-dimensional list. In other word: Series is essentially a one-dimensional labeled vector

- DataFrame: 
    DataFrame is the entire table (a matrix) formed by putting multiple Series side-by-side.

- Row: 
    A "row" in pandas is not a thing.
    It’s a temporary alignment of column values that share the same index label.

## Why .loc[1] feels like a row
This aligns all columns on index 1 and returns a Series whose index = column names
That Series is constructed on the fly.
It’s not stored anywhere.

.loc[1] 
- returns a series (Give me all columns where index label is 1)
- resulting Series uses the DataFrame’s column names as its index.

.loc[0:3] 
- returns a dataframe

.loc[0, ["ProductName", "Handle"]] 
-returns a series with index label (ProductName and Handle)

.loc[0, "ProductName"]
- returns a string

.loc[data["ProductName"].isin(["cat", "banana"]), "ProductName"] 
- returns a series where index is number

person_series = pd.Series(["ashish", "binay", "harish"], index=["ashish", "binay", "harish"])
(valid) person_series["ashish]
(valid) person_series.loc["ashish]

person_series = pd.Series(["ashish", "binay", "harish"])
(valid) person_series[0]
(valid) person_series.loc[0]
(valid) person_series.iloc[0]

Note on series:
Being able to access series data using ["key"] or [number-index] makes it look like typical dict/row

Note on dataframe:
You can also access a DataFrame by index but just not in the same way as a Series.
(access data by label) df.loc[0]
(access data by position) df.iloc[0]

##Visualize dataframe

A DataFrame is essentially:

ProductName            → values + index
ContextXSellProduct1   → values + index
ContextXSellProduct2   → values + index
ContextXSellProduct3   → values + index

df = {
    "ProductName": Series(["product-1", "product-2"]),
    "ContextXSellProduct1": Series(["001", "011"]),
    "ContextXSellProduct2": Series(["002", "022"]),
    "ContextXSellProduct3": Series(["003", "033"]),
}

There are no rows. 
Rows are an alignment illusion created by shared index.
Rows exist only because indexes of Series line up.

With that in mind:

axis = 0
> even easier: operate on each column, result = per column, index = column names.
> when you do df.mean(axis=0), you are essentially telling pandas to loop through your dictionary (key) and calculate the mean for each Series (value of dict key is a series of same type of data).
axis=0 → operate on each Series

axis = 1
> align multiple Series by index
> at each index position, combine values from multiple Series
> even easier: operate across columns, result = per row
> index becomes the column name for each data point 
axis=1 → combine multiple Series by index where column name becomes the new index for combined series

Why specifying axis in the code below result in no argument axis found error?

df["ProductName"].apply(do_something)

> axis=0 vs axis=1 only matters for DataFrames
> Series only has one dimension (the index), so there’s no axis to specify.


### Question1:

```
df = pd.DataFrame({ 
    "ProductName": ["product-1", "product-2"], 
    "ContextXSellProduct1": ["001", "011"], 
    "ContextXSellProduct2": ["002", "022"], 
    "ContextXSellProduct3": ["003", "033"] 
}) 
```

sum_axis_0 = df.sum(axis=0)

sum_axis_0.index why is the returned index has column names? 

axis=0 → operate down each column.

- Pandas takes each column (Series) and computes the sum along its index (row labels).
- The result is a Series where:
    - index = the column names (ProductName, ContextXSellProduct1, etc.)
    - values = sum of each column

So s.index gives column names because the resulting Series represents one value per column.

#### Intuition (columnar thinking)
- axis=0: sum inside each Series, result is per column, index = column names.

### Question2:

```
df = pd.DataFrame({ 
    "ProductName": ["product-1", "product-2"], 
    "ContextXSellProduct1": ["001", "011"], 
    "ContextXSellProduct2": ["002", "022"], 
    "ContextXSellProduct3": ["003", "033"] 
}) 
```

sum_axis_1 = df.sum(axis=1) 

sum_axis_1.index why is the returned index has int value? 

axis=1 → operate across columns for each row.

- Pandas takes one row at a time (creates a temporary Series where index = column names and values = that row) and sums the values.
- The result is a Series with length = number of rows, so its index = original row indices (0, 1, …).

So s.index returns integers because the resulting Series represents one value per row, not per column.

#### Intuition (columnar thinking)
- axis=1: sum across Series for each row, result is per row, index = row labels.


### Row based vs Column based storage
Row-Based Storage (Traditional):
[Alice, 30, New York], [Bob, 25, London], [Carol, 35, Paris] all data for one record is together

Columnar Storage (Physical Layout):
[Alice, Bob, Carol] (all Names together)
[30, 25, 35] (all Ages together)
[New York, London, Paris] (all Cities together)
