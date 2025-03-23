from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
# df.plot()
# (df**2).plot()
# plt.show()


# Plotting ACF and PACF of the closing value time series
# plot_acf_pacf(df.pct_chg)
# plot_acf_pacf(df.pct_chg**2)

#looks like a garch(2, 2) model is suitable
model = arch_model(df.pct_chg, vol='Garch', p=2, q=2)
fit = model.fit()
# print(fit.summary())

last_quart = df.index[-1]+ pd.offsets.QuarterBegin(1)

pred = fit.forecast(horizon=2).mean.iloc[-1].values

new_dates = pd.date_range(start = last_quart , periods = 2, freq='MS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred_gdp = pd.concat([df['pct_chg'], new_df])