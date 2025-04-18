from package_imports import *

'''
This file was not used in the model and used mainly to analyse GDP
'''

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("GDP", "2020-01-01", fred)
df = transform_series(df, 5).dropna()

df.plot()
plt.show()

plot_acf_pacf(df)

# testing for stationarity may be stationary as power is low
print("ADF Test Result: ", adfuller(df, regression="c"))
# First diff shows significant improvement thus can conclude that first diff is stationary
df = difference_df(df, 1)
# print("ADF Test Result: ", adfuller(df['Diff_Value']))
diff_df = df['Diff_Value']

#might want to take first difference of gdp


