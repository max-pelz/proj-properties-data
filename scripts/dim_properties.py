# %%

import pandas as pd
import os

# %%

input_path = os.path.join("..", "data", "stage", "stg_properties.pickle")
output_path = os.path.join("..", "data", "dimensions", "dim_properties.csv")

# %%

df = pd.read_pickle(input_path)

# %%

#print("Summary statistics for all columns:")
#print(df.describe(include='all'))
#print()

# %%

# Drop irrelevant columns
df.drop(
    columns=[
        'total_co2_costs_or_emissions', 'created_at_utc'
    ],
    inplace = True
)

# %%

df.to_csv(output_path, index=False)

#% %