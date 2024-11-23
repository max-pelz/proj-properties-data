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
print(df_with_both.shape)

# %%

# Check whether there are mismatches between the 2 JSON columns
df_with_both['json_matches'] = df_with_both.apply(
    lambda row: (
        row['total_co2_costs'] in str(row['total_co2_emissions'])
    ),
    axis=1
)

print("Number of these columns matching:")
matches = df_with_both[df_with_both['json_matches']]
print(matches.shape)
