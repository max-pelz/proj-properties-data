# %%

import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import math

# %%

# Input paths
addresses_path = os.path.join("..", "data", "dimensions", "dim_addresses.csv")
properties_path = os.path.join("..", "data", "dimensions", "dim_properties.csv")
users_path = os.path.join("..", "data", "dimensions", "dim_users.csv")
emissions_path = os.path.join("..", "data", "facts", "fct_co2_emissions.csv")

plots_base_path = os.path.join("..", "plots")

## %%

# Read data
dim_addresses = pd.read_csv(addresses_path)
dim_properties = pd.read_csv(properties_path)
dim_users = pd.read_csv(users_path)
fct_co2_emissions = pd.read_csv(emissions_path)

# %%

# Distribution of properties

# Merge the relevant DataFrames
properties_with_addresses = dim_properties.merge(
    dim_addresses, left_on='id', right_on='property_id',
    suffixes=('_property', '_address')
)

# Group by city and postal_code and count rows
city_grouped = properties_with_addresses.groupby('city').size().sort_values(ascending=False)
postal_code_grouped = properties_with_addresses.groupby('postal_code').size() \
    .sort_values(ascending=False).head(10)

# Visualization
# Bar chart for city grouping
plt.figure(figsize=(10, 6))
ax = city_grouped.plot(kind='bar')
plt.title('Number of Properties by City')
plt.xlabel('City')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Adding data labels
for i, value in enumerate(city_grouped.values):
    ax.text(i, value, str(value), ha='center', va='bottom')

plot_name = "properties_by_city.png"
plot_path = os.path.join(plots_base_path, plot_name)
plt.savefig(plot_path)
plt.close()

# Bar chart for postal_code grouping
plt.figure(figsize=(10, 6))
postal_code_grouped.plot(kind='bar')
plt.title('Number of Properties by Postal Code')
plt.xlabel('Postal Code')
plt.ylabel('Count')
plt.xticks(rotation=45)

plot_name = "properties_by_plz.png"
plot_path = os.path.join(plots_base_path, plot_name)
plt.savefig(plot_path)
plt.close()

# %%
# Users in properties

properties_full = properties_with_addresses.merge(
    dim_users, left_on='created_by_property', right_on='id'
)

# %%

# Temporarily disable pandas truncation
#pd.set_option('display.max_columns', None)
#properties_full

# %%

# Drop some duplicate and irrelevant columns
properties_full.drop(
    columns=[
        'created_by_property', 'created_by_address', 'property_id',
        'first_name', 'last_name'
    ],
    inplace = True
)

# Rename some columns for clarity
properties_full = properties_full.rename(
    columns={
        'id_property': 'property_id',
        'id_address': 'address_id',
        'id': 'user_id'
    }
)

# %%

# Count rows grouped by whether `full_name` and `email` are null or not
grouped_counts = properties_full.assign(
    full_name_not_null=properties_full['full_name'].notna(),
    email_not_null=properties_full['email'].notna()
).groupby(['full_name_not_null', 'email_not_null']).size().reset_index(name='count')

print(grouped_counts)

# %%

# Boxplots for numerical columns

# List of numerical columns
numerical_columns = [
    'co2_factor_heating',
    'co2_intensity',
    'construction_year',
    'energy_intensity',
    'splitting_factor',
    'splitting_factor_commercial',
    'splitting_factor_residential',
    'total_commercial_floor_area',
    'total_energy_demand_consumption',
    'total_floor_area',
    'total_residential_floor_area'
]

# Determine the layout for subplots (e.g., 3 columns)
num_columns = 3
num_rows = math.ceil(len(numerical_columns) / num_columns)

# Create the canvas
fig, axes = plt.subplots(num_rows, num_columns, figsize=(15, 5 * num_rows))
axes = axes.flatten()  # Flatten to iterate easily

# Create individual box plots
for i, column in enumerate(numerical_columns):
    if column in properties_full.columns:
        properties_full.boxplot(column=column, ax=axes[i])
        axes[i].set_title(f'Box Plot: {column}')
        axes[i].set_ylabel('Value')
    else:
        axes[i].axis('off')  # Turn off axis for empty subplots

# Remove any extra axes
for j in range(len(numerical_columns), len(axes)):
    axes[j].axis('off')

plt.tight_layout()

plot_name = "box_plots.png"
plot_path = os.path.join(plots_base_path, plot_name)
plt.savefig(plot_path)
plt.close()  # Close the figure to save memory

# %%

# CO2 intensity vs construction year

# Filter the data to exclude rows with NaN values in the relevant columns
scatter_data = properties_full[['co2_intensity', 'construction_year']].dropna()

# Scatter plot data
x = scatter_data['construction_year']
y = scatter_data['co2_intensity']

# Fit a linear regression line (trend line)
m, b = np.polyfit(x, y, 1)  # Slope (m) and intercept (b)

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.6, label='Data Points')
plt.plot(x, m * x + b, color='red', label=f'Trend Line (y = {m:.2f}x + {b:.2f})')
plt.title('Scatter Plot of CO2 Intensity vs. Construction Year with Trend Line')
plt.xlabel('Construction Year')
plt.ylabel('CO2 Intensity')
plt.legend()
plt.grid(True)

# Save the scatter plot
plot_name = "scatter_co2_intensity_vs_construction_year.png"
plot_path = os.path.join(plots_base_path, plot_name)
plt.savefig(plot_path)
plt.close()  # Close the figure to save memory

# %%

# Bar charts to see category distributions

# Text and boolean categories
text_categories = [
    'commercial_usage_type',
    'company_name',
    'heating_energy_source',
    'orientation',
    'potential',
    'potential_rating',
    'property_type'
]

boolean_categories = [
    'air_conditioning_available',
    'energy_modernization',
    'ventilation_available'
]

# Combine all categories for iteration
all_categories = text_categories + boolean_categories

# Replace NaN with 'N/A' for all specified columns
properties_full[all_categories] = properties_full[all_categories].fillna('N/A')

# Determine the layout for subplots (e.g., 3 columns)
num_columns = 3
num_rows = math.ceil(len(all_categories) / num_columns)

# Create the canvas
fig, axes = plt.subplots(num_rows, num_columns, figsize=(18, 5 * num_rows))
axes = axes.flatten()  # Flatten to iterate easily

# Create individual bar charts
for i, category in enumerate(all_categories):
    if category in properties_full.columns:
        # Get the top 10 categories
        counts = properties_full[category].value_counts().head(10)
        
        # Create the bar plot
        counts.plot(kind='bar', ax=axes[i], color='skyblue', alpha=0.8)
        axes[i].set_title(f'Counts for {category}')
        axes[i].set_ylabel('Count')
        axes[i].set_xlabel(category)
        axes[i].tick_params(axis='x', rotation=45)
        
        # Add data labels
        for p in axes[i].patches:
            axes[i].annotate(f'{int(p.get_height())}', 
                             (p.get_x() + p.get_width() / 2., p.get_height()), 
                             ha='center', va='bottom')
    else:
        axes[i].axis('off')  # Turn off axis for categories not found in the DataFrame

# Turn off any unused axes
for j in range(len(all_categories), len(axes)):
    axes[j].axis('off')

plt.tight_layout()

# Save the canvas as a single image
plot_name = "bar_charts_text_and_boolean_categories.png"
plot_path = os.path.join(plots_base_path, plot_name)
plt.savefig(plot_path)
plt.close()  # Close the figure to save memory

# %%

# Group by user_id and count the number of properties per user
properties_per_user = properties_full.groupby('user_id').size()

# Calculate the average number of properties per user
average_properties_per_user = properties_per_user.mean()

print(f'Average number of properties per user: {average_properties_per_user:.2f}')

# %%

# Yearly CO2 emissions

# Filter the data for years 2024 to 2034
years = range(2024, 2035)
fct_co2_emissions_filtered = fct_co2_emissions[fct_co2_emissions['year'].isin(years)]

# Create the figure
plt.figure(figsize=(15, 8))

# Create a box plot for each year
fct_co2_emissions_filtered.boxplot(
    column='co2_emission_metric_tons',
    by='year',
    grid=True,
    figsize=(15, 8)
)

# Customize the plot
plt.title('Distribution of CO2 Emissions (Metric Tons) by Year (2024-2034)')
plt.suptitle('')  # Remove default boxplot title
plt.xlabel('Year')
plt.ylabel('CO2 Emission (Metric Tons)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plot_name = "boxplot_co2_emissions_by_year.png"
plot_path = os.path.join(plots_base_path, plot_name)
plt.savefig(plot_path)
plt.close()  # Close the figure to save memory

# %%
