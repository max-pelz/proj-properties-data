# %%

import pandas as pd
import os
import json
import numpy as np
import re

# %%

input_path = os.path.join("..", "data", "source", "src_addresses.csv")
output_path = os.path.join("..", "data", "stage", "stg_addresses.pickle")

# %%

df = pd.read_csv(input_path, encoding="utf-8")

# %%

# Summary statistics of the data

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

# Check combinations of null values for 'address' and 'address_object'
null_combinations = (
    df.assign(
        address_null=df['address'].isna(),
        address_object_null=df['address_object'].isna()
    )
    .groupby(['address_null', 'address_object_null', 'is_address_autocomplete'])
    .size()
    .reset_index(name='count')
)

# Display the result
print(null_combinations)

# %%

# Understand the address_object better

# Temporarily disable pandas truncation
pd.set_option('display.max_colwidth', None)

# Display the parsed JSON column
print(df['address_object'].head())

pd.reset_option('display.max_colwidth')

# %%

# Parse the address_object JSON into a dictionary
df['parsed_address'] = df['address_object'].apply(
    lambda x: json.loads(x) if pd.notna(x) else None
)

# Format 1: "street_name street_number, postal_code city"
df['formatted_address'] = df['parsed_address'].apply(
    lambda x: (
        f"{x['street_name']} {x['street_number']}, {x['postal_code']} "
        f"{x['city']}"
     ) if x else None
)

# Format 2: "street_name street_number, postal_code city, country"
df['formatted_address_country'] = df['parsed_address'].apply(
    lambda x: (
        f"{x['street_name']} {x['street_number']}, {x['postal_code']} "
        f" {x['city']}, {x['country']}" 
    ) if x else None
)

# Replace None with NaN for simplified handling downstream
columns_to_replace = [
    'parsed_address', 'formatted_address', 'formatted_address_country'
]
df[columns_to_replace] = df[columns_to_replace].replace([None], np.nan)

# Display the results
print(df[['address_object', 'formatted_address', 'formatted_address_country']])

# %%

# Prepare matching address and address object for collisions
df_with_both_addresses = df[['id', 'address', 'formatted_address']]

df_with_both_addresses = df_with_both_addresses.dropna(
    subset=['address', 'formatted_address'],
    how='any'
)

print("Addresses where both address columns are available:")
print(df_with_both_addresses.shape)

# %%

# Check whether there are mismatches between the 2 core address columns.
df_with_both_addresses['address_matches_object'] = df_with_both_addresses.apply(
    lambda row: (
        row['address'] in str(row['formatted_address'])
    ),
    axis=1
)

print("Number of these addresses not matching:")
mismatches = df_with_both_addresses[~df_with_both_addresses['address_matches_object']]
print(mismatches.shape)

# %%

# Create the final DataFrame before splitting address into columns

# Coalesce 'formatted_address' and 'address' into a single 'address' column
df['full_address'] = df['formatted_address_country'].fillna(df['address'])

# Create the final DataFrame with the desired columns
df = df[[
    'id', 'created_by', 'property_id', 'full_address', 'is_address_autocomplete',
    'created_at_utc'
]]

# %%

# Function to split the address into components
def split_address(address):
    # Regular expression to match the pattern
    match = re.match(r'^(.+?) (\d+), (\d+) ([^,]+)(?:, (.+))?$', address)
    if match:
        street, street_number, postal_code, city, country_iso = match.groups()
        return {
            'street': street,
            'street_number': street_number,
            'postal_code': postal_code,
            'city': city,
            'country_iso': country_iso if country_iso else 'DE'  # Default to DE
        }
    return {
        'street': np.nan,
        'street_number': np.nan,
        'postal_code': np.nan,
        'city': np.nan,
        'country_iso': 'DE'  # Default country_iso to DE for invalid addresses
    }

# Apply the function to split addresses
split_columns = df['full_address'].apply(split_address).apply(pd.Series)

# Combine the new columns with the original DataFrame
df = pd.concat([df, split_columns], axis=1)

df.head()

# %%

# Data quality

# Ensure the user id is unique
assert df['id'].is_unique, "User id is not unique"

# Ensure that all columns are non-null
for col in df.columns:
    assert df[col].notnull().all(), f"{col} has null values"

# %%

# Save the transformed data
df.to_pickle(output_path)

# %%
