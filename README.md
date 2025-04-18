# 6s3ns3
DSE3101 project - Nowcasting

Our model would adopt a bridge model similar to that of the Atlanta FRED model.

It would use a similar methodology of Consumption(C), Investment(I), Government(G), Nett Exports(X-M).

We aim to predict the GDP for the current quarter as well as as past quarter that has not been released. 

We assume that data follows a 1 month lag. For example, all monthly and quarterly data would only have an initial prediction 1 month in advance.

We aim to do 2 things, predict GDP in current quarter and past quarters. For example, in the start of M3 2024, we would want to predict Q1 2024 GDP for that quarter. However, in the start of M1 2024, we would want  Q4 2023 GDP as this data is not released due to the lag in data release. For start of M1 of new quarter or end of M3 for previous quarter we want to predict the previous quarter GDP. For start of M2 or end of M1 we would know the past quarter GDP and would want to predict GDP for that whole quarter. Same for start of M3 and end of M2.

In order to do this quarterly prediction we intend to use a quarterly bridge model which splits quarterly GDP into its various components C, I, G, X-M. For each of these components, we intend to create a bridge model and use iterative predictions to get the quarterly value

Currently from the fred data, we have these for each component
"DGDSRC1": "Consumption Expenditure Goods", Monthly
"PCESC96": "Consumption Expenditure Services", Monthly
"EXPGSC1": "Goods & Services Exports", Quarterly
"IMPGSC1": "Goods & Services Imports", Quarterly
"PNFIC1": "Real Private Nonresidential Fixed Investment", Quarterly
"PRFIC1": "Real Private Residential Fixed Investment", Quarterly
"GCEC1": "Real Government Consumption Expenditures and Gross Investment", Quarterly
"SLEXPND": "State and Local Government Current Expenditures", Quarterly

Dependent variable
"GDP": "Gross Domestic Product", Quarterly

## Backend 
Firstly, we created our custom package name package_imports for our backend import statements and custom functions that we use. View imports.py to see which packages have been imported and utils.py for which functions were created

### utils.py
difference_df: takes the diff of the value
get_most_recent_series_of_date: gets the most recent df of a series
best_arma: CV and chooses the best ARMA orders in the model
pct_chg: Takes the percentage change using log diff
plot_acf_pacf: Plots the acf and pacf
eval: Gives RMSE, MAE and DA and plots the test and pred
transform_series: transform series as recommended by FRED
dm_test: Conducts DM test

### __init__.py
loads env folder and set seeds and import custom functions and installs packages

### Regressors
business_equiment.py
business_inventories.py
commercial_industrial_loans.py
consumption.py
exports_bop.py
govt_spending_construction.py
govt_spending_fed_defence.py
housing_unit_started.py
imports_bop.py
nondefense_captial_goods.py

### Benchmarks
arft04.py
benchmark1.py

### Models
midas_EN.py
midas.py
model1_EN.py
model1.py
Prophet.py
rf_bridge.py
rf_midas.py

### Predictions
arft04.py
benchmark1.py
bridge_model_prediction.py
midas_model_prediction.py
rf_model_prediction.py

### Other files
analysis_gdp.py: For initial analysis of GDP
dm.py: To conduct DM test
data_load.py: For compiling of data to be imported for our models
download_test_data.py: To preload our test data