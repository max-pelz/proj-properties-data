# Stage

## Users

We have unique, non-null user 'id' column as primary key. There are null values in the name and email columns (~47% individually, none across all columns together). Often, the email address is used as a commercial identifier for sales operations. So missing that many email addresses is a concern that needs to be addressed with stakeholders.

The 'created_at' timestamp needs to be converted to datetime for further analysis and we need to handle 5 (~= 33.3%) null values as they will create issues in a key timestamp (we might also want to update data and implement incremental imports). Thus, we simply default them to 1970, well before our business activities started (first available timestamp is in 2024).

## Addresses

We have a unique, non-null address 'id' column as primary key. We also have 2 non-null foreign key columns. The 'created_at' timestamp needs to be cleaned again (54.7% null values, defaulted to 1970 since first timestamp in 2024). Beyond that, the most interesting issue here is:

3 columns associated with the actual address content:

- address: Appears to contain the address string
- address_object: A json object containing similar information, but including country.
- is_address_autocomplete: Might flag if the 'address_object' was populated automatically without user input. In a real-world scenario, I would talk to the relevant stakeholders to better understand the underlying business process. Especially since the combinations of the 3 columns puts my initial interpretation in question.

Furthermore, 'address' and 'address_object' don't always match. Though there's no row where none of the 2 columns is set. Ideally, we create a source of truth to reliably match an address to a property. In 74.7% of cases, this simply means using a coalesce on both columns. For the remaining cases, both columns differ everytime (some matches in city at least).

Again, the underlying business process needs to be better understood to make the optimal decision here (or improve the process to generate better data). In the meantime, we will go with the address_object as source of truth. We default the country to DE as it's only available in one of the columns.

## Properties

The largest table so far with a lot of dimension columns. Again we have a unique, non-null primary key. Most of the other columns are null roughly half of the time.

- Numeric columns
    - co2_factor_heating
    - co2_intensity
    - construction_year: Convert to int
    - energy_intensity
    - splitting_factor
    - splitting_factor_commercial
    - splitting_factor_residential
    - total_commercial_floor_area
    - total_energy_demand_consumption
    - total_floor_area
    - total_residential_floor_area
- Categorical (Booleans)
    - air_conditioning_available
    - energy_modernization
    - ventilation_available
- Categorical (text)
    - commercial_usage_type
    - company_name
    - heating_energy_source
    - orientation
    - potential
    - potential_rating
    - property_type
- JSON: 'total_co2_costs' and 'total_co2_emissions' seem to have multiple years of data in a JSON object. We will extract that data into a separate fact table. It's already apparent that the quality of both columns is not great as costs and emissions are the same whenever both are not null. It's not entirely clear whether it's costs or emissions. We will consolidate and extract before making a judgement on that (without any additional business context we would get in a real-life scenario).

The numeric columns seem generally okay, apart from many nulls. We will analyze them for distributions and outliers. We can show the share of null values but largely focus on the samples where have values (for larger datasets, we expect those approach the population's distribution). construction_year we convert to int. Some of the columns, including construction year, we might want to group into categories (1900-1950, 1951-1980, ...) for analysis.

The categorical text columns seem okay apart from null values and some inconsistencies in the 'potential' column. We could default the null values to something like 'N/A' but, depending on the BI tool, visualizing null is usually fine and makes data quality issues easier to spot. The 'potential' column uses lower case English words except for 'Potential Rot' so it probably needs to be cleaned. Something to discuss with stakeholders.

We could default the booleans to either False or something like 'N/A' again, but we stick with our evaluation from above.

With more business context, we could create a less messy data model by e.g. splitting off the co2 relevant dimensions, or everything around commercial use. This depends to some degree on the BI tool used and the intended user groups (normalized tables in a star schema for analysts, denormalized wide tables for business users).