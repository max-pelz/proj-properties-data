# %%

import pandas as pd
import os
import json

# %%

input_path = os.path.join("..", "data", "stage", "stg_properties.pickle")
output_path = os.path.join("..", "data", "facts", "fct_co2_emissions.csv")

# %%

df = pd.read_pickle(input_path)

# %%

# Select relevant columns
df = df[['id', 'total_co2_costs_or_emissions']]

# Drop empty rows
df = df.dropna(subset=['total_co2_costs_or_emissions'])

# Summary statistics
print("Number of non-null rows:")
print(df.shape[0])
df.head()

# %%

# Parse the JSON into a dictionary
df['total_co2_costs_or_emissions'] = df['total_co2_costs_or_emissions'].apply(
    lambda x: json.loads(x) if pd.notna(x) else None
)

# %%

# Temporarily disable pandas truncation
#pd.set_option('display.max_colwidth', None)

# %%

print(df['total_co2_costs_or_emissions'])

#pd.reset_option('display.max_colwidth')

# %%

# Expand the dictionary into rows
expanded_rows = df.apply(
    lambda row: pd.DataFrame(
        [{'id': row['id'], 'year': year, 'co2_emissions': round(float(cost), 2)} 
         for year, cost in row['total_co2_costs_or_emissions'].items()]
    ),
    axis=1
)

# Combine all expanded rows into a final DataFrame
final_df = pd.concat(expanded_rows.values, ignore_index=True)
final_df

# %%

# Summary statistics for the co2_cost column
summary_stats = final_df['co2_emissions'].describe()

# Display the summary statistics
#print("Summary Statistics for co2_emissions:")
#print(summary_stats)

# %%

# Rename the columns appropriately
final_df = final_df.rename(
    columns={
        'id': 'property_id',
        'co2_emissions': 'co2_emission_metric_tons'
    }
)

# %%

# Data quality

# Ensure unique combinations of property_id and year
assert (
    final_df.reset_index()
    .duplicated(subset=['property_id', 'co2_emission_metric_tons'])
    .sum()
    == 0
), "There are duplicate property_id and year combinations"

# Ensure that all columns are non-null
for col in final_df.columns:
    assert final_df[col].notnull().all(), f"{col} has null values"

# %%

final_df.to_csv(output_path, index=False)

# %%