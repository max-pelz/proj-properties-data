# %%

import pandas as pd
import os

# %%

input_path = os.path.join("..", "data", "source", "src_properties.csv")
output_path = os.path.join("..", "data", "stage", "stg_properties.pickle")

# %%

df = pd.read_csv(input_path, encoding="utf-8")

# %%

# Summary statistics of the data

print()
print()
print("PROPERTIES")
print()

# Temporarily disable pandas truncation
pd.set_option('display.max_columns', None)

num_rows, num_columns = df.shape
print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")
print()

print("Data types of each column:")
print(df.dtypes)
print()

print("Number of NaN values per column:")
print(df.isna().sum())
print()

print("Summary statistics for all columns:")
print(df.describe(include='all'))
print()

print("Detailed DataFrame information:")
print(df.info())
print()

print("First 10 rows of the DataFrame:")
df.head(10)

pd.reset_option('display.max_columns')

# %%

#pd.set_option('display.max_rows', None)

# %%

#df

# %%

#pd.reset_option('display.max_rows')

# %%

# Cast created_at timestamp to datetime
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# Check the minimum timestamp
min_timestamp = df['created_at'].min()
print(f"The minimum timestamp in created_at is: {min_timestamp}")

# %%

# A missing created_at value will likely lead to errors.
# So we default it 1970, well before our business activities started.
df['created_at'] = df['created_at'].fillna(pd.Timestamp('1970-01-01'))

# Assume the timestamp is UTC
df = df.rename(columns={'created_at': 'created_at_utc'})

# %% 

# Investigate the co2 JSON columns
df_with_both = df[['id', 'total_co2_costs', 'total_co2_emissions']]

df_with_both = df_with_both.dropna(
    subset=['total_co2_costs', 'total_co2_emissions'],
    how='any'
)

print("Properties where both co2 JSON columns are available:")
print(df_with_both.shape[0])

# %%

# Check whether there are mismatches between the 2 JSON columns
df_with_both['json_matches'] = df_with_both.apply(
    lambda row: (
        row['total_co2_costs'] in str(row['total_co2_emissions'])
    ),
    axis=1
)

print("Number of rows where these columns match:")
matches = df_with_both[df_with_both['json_matches']]
print(matches.shape[0])

# %%

# Coalesce total_co2_cost and total_co2_emissions
df['total_co2_costs_or_emissions'] = df['total_co2_costs'] \
    .fillna(df['total_co2_emissions'])

# Drop the previous columns
df.drop(
    columns=['total_co2_costs', 'total_co2_emissions'],
    inplace = True
)

# %%

# Convert the column to nullable integer type (Int64)
df['construction_year'] = df['construction_year'].astype('Int64')

print("Data types of each column:")
print(df.dtypes)
print()

# %%

# Data quality

# Ensure the user id is unique
assert df['id'].is_unique, "User id is not unique"

columns = ['id', 'created_at_utc']

# Ensure that columns are non-null
for col in columns:
    assert df[col].notnull().all(), f"{col} has null values"

# %%

# Save the transformed data
df.to_pickle(output_path)

# %%