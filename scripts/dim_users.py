# %%

import pandas as pd
import os
import numpy as np

# %%

input_path = os.path.join("..", "data", "stage", "stg_users.pickle")
output_path = os.path.join("..", "data", "dimensions", "dim_users.csv")

# %%

df = pd.read_pickle(input_path)

# %%

# Create a full_name column
df['full_name'] = df['first_name'].str.cat(df['last_name'], sep=' ', na_rep='')
df['full_name'] = df['full_name'].replace(' ', np.nan)

# %%

# Select relevant columns
df = df[['id', 'email', 'full_name', 'first_name', 'last_name']]

# %%

#print("Summary statistics for all columns:")
#print(df.describe(include='all'))
#print()

#print("Number of NaN values per column:")
#print(df.isna().sum())

# %%

df.to_csv(output_path, index=False)

# %%