# %%

import pandas as pd
import os

# %%

input_path = os.path.join("..", "data", "stage", "stg_addresses.pickle")
output_path = os.path.join("..", "data", "dimensions", "dim_addresses.csv")

# %%

df = pd.read_pickle(input_path)

# %%

# Summary statistics for the co2_cost column
summary_stats = df['created_at_utc'].describe()

# Display the summary statistics
#print("Summary Statistics for created_at_utc:")
#print(summary_stats)

# %%

# Select relevant columns
df = df[[
    'id', 'created_by', 'property_id', 'street', 'street_number',
    'postal_code', 'city', 'country_iso'
]]

# Strip outer spaces from all string columns in the DataFrame
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# %%

df.to_csv(output_path, index=False)

#% %