# 6s3ns3
## Project Overview: 
Currently, economists and policymakers are facing challenges in receiving up-to-date information about Gross Domestic Product (GDP). As data on GDP is only available quarterly, there is a lag in which the GDP estimate of the quarter will be available. This lag, often up to 4 months, creates substantial challenges for timely decision making. Thus, 6se3nse is our one-stop solution for staying ahead of the economy. 6se3nse provides economists and policymakers with more timely estimates of quarterly GDP growth through monthly updated nowcast. For example, in early November, economists can access a nowcast for Quarter 4 (Q4), instead of waiting till late January for the official Q4 GDP release. In addition, users can stay abreast of the latest economic news from top financial sources and explore latest  economic data so users can focus on work that truly matters. 6se3nse leverages a Python and Flask framework backend with the Dash framework for its front-end interactive components.

Dependent variable:
"GDP": "Gross Domestic Product", Quarterly Change of Seasonally Adjusted GDP

## File Structure: 
### FrontEnd:
We implemented the front-end web application using Dash, and all related code can be found in the frontend folder. The frontend folder contains the main app.py file used to run our Dash application, as well as a requirements.txt file that lists all the packages required for this project. Other subfolders are also included and will be explained in detail in the sections below.

### assets:
#### pictures
This folder contains all the profile images of our team members, which are displayed on the About page of the application. 

#### meettheteam.py
This file contains the code for implementation of our Meet the Team section of the About page of the application. 

#### react.css
This file contains all the custom styling used throughout the web application. Styles are applied using unique className id to ensure consistent design across components.

#### data
This folder contains all the code responsible for retrieving respective economic indicator data from FRED, which is displayed in the corresponding section of the web application. 



## Backend 
Firstly, we created our custom package name package_imports for our backend import statements and custom functions that we use. View imports.py to see which packages have been imported and utils.py for which functions were created

### package_imports
This is our own custom package for the backend to help with the import of packages and to custom functions as well as initialisation of essential variables

#### imports.py
Import of packages

#### utils.py
This is to file to store all our custom functions. Here is a descriptions of the functions that we created.
difference_df: takes the diff of the value
get_most_recent_series_of_date: gets the most recent df of a series
best_arma: CV and chooses the best ARMA orders in the model
pct_chg: Takes the percentage change using log diff
plot_acf_pacf: Plots the acf and pacf
eval: Gives RMSE, MAE and DA and plots the test and pred
transform_series: transform series as recommended by FRED
dm_test: Conducts DM test

#### __init__.py
loads env folder and set seeds and import custom functions and installs packages

### Regressors
We perform the initial analysis of the regressors here. 
1. We get our data from FRED first. We would try to get the data as close to the date that we actually want. Since our training data is from 2007 M6 we get data up to 2007 M12 then filter this is to ensure that we have all the data up to M6. Should the data be available but only published onto FRED (i.e. Imports and Exports) we will get the data as close to the data as possible then filter up to 2007 M6

2. We perform the recommended transform then plot the graph to check for missing values. 

3. We perform ADF test with a constant to account for a non-constant mean. We dont use a time trend as we don't think that in the long run our data should have an increasing trend or decreasing trend. If stationary, then leave as is. Else, we attempt to visually verify if it is really non-stationary. Since ADF test tend to have lower power, we tend to handle with a bit of discretion to see if additional differencing is necessary. We also look at the PACF and ACF to find orders for ARMA. We verified previously that the series is stationary so d = 0.

4. CV is performed by our best_arma function found in utils.py. We use recursive expanding window OOS forecast for 1-step forecast for 30 obs after the parameters that we maked. In the event that there is not enough data we may choose to reduce the number of observations or to reduce the (p, q) to deviate from the ACF and PACF found by our models.

5. We then fit an ARMA model and try to forward fill our data based on our ARMA models, this would typically result in prediction of 2-4 monmths based on the month the user is in

6. After that at the bottom we create a function to help forward fill that component given the data as of that date

#### business_equiment.py: For Industrial Production: Equipment: Business Equipment
#### business_inventories.py: For Total Business Inventories
#### commercial_industrial_loans.py: For Commercial and Industrial Loans, All Commercial Banks
#### consumption.py: For Personal Consumption Expenditure
#### exports_bop.py: For Exports of Goods and Services: Balance of Payments Basis
#### govt_spending_construction.py: For Total Public Construction Spending: Total Construction in the United States
#### govt_spending_fed_defence.py: For Federal Government: National Defense Consumption Expenditures and Gross Investment
#### housing_unit_started.py: New Privately-Owned Housing Unit Started
#### imports_bop.py: For Imports of Goods and Services: Balance of Payments Basis
#### nondefense_captial_goods.py: For Manufacturers’ New Orders: Nondefense Capital Goods

### Benchmarks
For these 2 benchmarks the idea is very simple, just fit the ARFT04 or take the historical mean.
We do the evaluation of these data for our test data 2007 Q3 to 2019 Q4. So we just recursively fit new models and predict one step into the future and take the RMSE, MAE and DA.
We then save the predictions to be use in the future
#### arft04.py
#### benchmark1.py

### Models
#### midas.py
#### model1.py: Bridge model
Initially we start with model1 aka bridge and MIDAS. After getting the data from data_load.py we import the data from the functions over to models. For the 2 initial models, we analyse the VIF, correlation plot and condition numbers to check for multicollineartiy. Next, we do the evaluation of the test data based on our test data. You find above the variable given date which is essentially serves as a way to help the person to time travel. So in this case we can time travel back to our test date and save the predictions for our test data. After evaluation, we go back to the present to find how our model would perform now. We fit an OLS and try to find out more about the coefficients about the components and analyse the residuals. Only for our bridge model, we try to form a basic CI for our prediction but admittedly it is not complete. For more details, check out CI for bridge model.pdf to see our formula for homoskedastic errors. In the future however, we would recommend the use heteroskedastic errors as part of the formula.

#### rf_bridge.py
#### rf_midas.py
Next we analyse our models. We follow the same method as the previous 2 models but the main difference was the choosing of the number of trees. To perform this CV, we adopt a similar method to our evaluation and CV. Given our test data, which is up to 2007 Q3, we hold out the last 30 observations and run recurive expanding window CV to find the number of trees that minimise RMSE. Then we evaluate and save predictions. We tried both ways of aggregation, both the way we aggregate for MIDAS and Bridge but decided found actually both have the same result so we decided to place more restrcitions for simplicity and use the Bridge aggregation method. 

#### midas_EN.py
#### model1_EN.py
We tried to add a form of regularisation through ElasticNet for both of our models. We did the same as the normal bridge and MIDAS but with the same CV method as our RF to find the optimal alpha and l1_weight that minimise RMSE. However, in the end we decided not to use it due to marginal improvment and conflicting econometric theory on whether this is correct

#### Prophet.py
Lastly we tried out Prophet by Meta. As one of the more commonly used commerical software for time series prediction in the workplace, we wanted to dip our toes and try it out to see if it could have very substantial improvements due to its additive components. However we decided against publishing it in the end for our project as we arent very familiar with the econometric theory and whether its use would be suitable for nowcasting.


### Predictions
#### arft04.py
#### benchmark1.py
#### bridge_model_prediction.py
#### midas_model_prediction.py
#### rf_model_prediction.py

### Other files
#### analysis_gdp.py: For initial analysis of GDP
#### dm.py: To conduct DM test
#### download_test_data.py: To preload our test data

#### data_load.py: For compiling of data to be imported for our models
We start of by copying the functions from all of our regressor components to help forward fill the components. For each of the functions we allow a period parameter to help account for whether the user is choosing for the MIDAS or bridge model.

Here we also include our code for the sahms rule from line 195.
So for the aggregation of sahms indicator for bridge we decided to use an exponential loading aka M1 has a weight of .1, M2 has a weight of .3 and M3 has a weight of .6 So our Sahm's recession indicatoris a binary variable . We hope that by doing this kind of loading we help create more important on more recent months EG in our training data, we generally saw streaks where the Sahms indicator was 1 (ie recession) so if the value was 0 in the first month but 1 in the next 2 months we predict a recession is coming and want to put more penalisation. However if the first month is 1 and the next 2 months is 0 means the recession finishing so we wanna put less weight. This thinking holds true for the predicted value oso. Lets say i in M3 and only have data for M1. If M1 is 1, we assume a recession is still happening in the quarter and aggregate it by making all the unknown months 1. If M1 is 0 we assume recession is not happening and make the whole quarter 0.

Next, we have our load data functions which we will use in our respective models. We first check if we have the dataset in our "database" if not we go about predicting. We compile each of the components including a lag of GDP using the same method as we would predict our components. Then we aggregate or compile based on Bridge or MIDAS and save our data to our data base for quick access and return the data to be used by the models

### Data Storages
To help our website speed up, we would preload the data in advance so that we dont need to generate the data all the time and can just read it.

Predictions: Predictions generated by our models for DM test and evaluation
Here we have the predictions for our model for the test period with the test.csv being the ground truth

#### test_data_bridge: Preloaded data for Bridge
#### test_data_nohouse: Bridge data generated without housing starts
#### test_data_midas: Preloaded data for MIDAS
#### Here we have the monthly data stored allowing for quick access