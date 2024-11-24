All analysis is done in scripts/analysis.py, including generation of relevant visualization.

# Exploratory data analysis

## Distribution of properties

We only have 5 cities in the data and with 120 properties, Berlin has by far the most. Only 2 postal codes appear twice, the rest occurs once. It would be easy enough to load a dataset of all German postal codes to map them to federal states. This would be a good source: https://public.opendatasoft.com/explore/dataset/georef-germany-postleitzahl/export/. However, I've decided against it since it would force the reader to download the data themselves to run the repo.

## Missing data

For critical fields, there's mainly address and user information. One could also count the CO2-related information as critical, but that really depends on the feature we need to identify prime opportunities to improve the energetic footprint of building.

Consolidated address information is available for all properties. If we accept any name component or the email, then all properties have a user assigned. Only 33.3% have both and 53.3% email information. If the user is indeed the customer, that's a serious problem as it'll be hard to identify them across systems, not even considering communication barriers.

# Trends and patterns

All numerical column apart from construction year appear to be factors/rating/shares between 0 and 100, which for some of the columns seems weird (randomly generated?). Clearly, we need more context from stakeholders. There are some metrics that seem almost identically distributed (co2_intensity and energy_intensity).

Properties were contructed between mid 1980s to mid 2000s, with the median being late 1990s. This makes some sense as we expect older buildings to have worse energetic food prints.

Looking at a scatter plot of CO2 intensity vs construction year indeed shows a negative correlation (correlation coefficient = -0.2). I guessed CO2 intensity as an important feature to identify opportunities. If that's confirmed, we could run a model to identify correlations among our dimensions (features) to see what we really need to be looking at (and thus collect high-quality data on).

Looking at the distributions of counts for the categorical variables, nothing sticks out immediately. There are a number of companies with 3 properties in the dataset. The top 3 heating sources are Fernwärme, Elektro, and Öl-Heizung. Generally, these features should really be looked at closely with a simple model to find correlations. However, that just needs more business context.

There are 15 users and the average of properties per user is 10. At 150 properties, each user has 10 properties.

Looking at CO2 emissions over time might be the most interesting: They go up significantly over time! However, the values for each year are identical across all properties. This is highly suspect and something to be investigated.