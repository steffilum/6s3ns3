from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
mean = df.pct_chg.mean()
df['demean_pct_chg'] = df.pct_chg - mean


# Function to plot ACF and PACF
def plot_acf_pacf(timeseries):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    plot_acf(timeseries, ax=ax1, lags=75)
    plot_pacf(timeseries, ax=ax2, lags=75)
    plt.show()


# Plotting ACF and PACF of the closing value time series
plot_acf_pacf(df['demean_pct_chg'])

MA = ARIMA(endog=df['demean_pct_chg'], order = (0, 0, 4)).fit()
print(MA.summary())

print(MA.forecast(steps = 2)+mean)