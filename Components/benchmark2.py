from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
mean = df.pct_chg.mean()
df['demean_pct_chg'] = df.pct_chg - mean





# Plotting ACF and PACF of the closing value time series
plot_acf_pacf(df['demean_pct_chg'])

#best number of lags for ma is roughly 4
MA = ARIMA(endog=df['demean_pct_chg'], order = (0, 0, 4)).fit()
print(MA.summary())

print(MA.forecast(steps = 2)+mean)