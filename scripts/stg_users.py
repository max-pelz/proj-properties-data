# %%

import pandas as pd
import os

# %%

input_path = os.path.join("..", "data", "source", "src_users.csv")
output_path = os.path.join("..", "data", "stage", "stg_users.pickle")

# %%

df = pd.read_csv(input_path, encoding="utf-8")

# %%

# Summary statistics of the data

print()
print()
print("USERS")
print()

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

# %%

# Check rows where all specified columns are empty (NaN)
empty_rows_count = df[['first_name', 'last_name', 'email']] \
    .isna().all(axis=1).sum()

# Display the count
print(f"Number of rows with all sales properties empty: {empty_rows_count}")


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