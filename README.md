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
