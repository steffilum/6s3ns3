from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("MTSO133FMS", "2020-01-01", fred)

#transform series
pct_chg_fed_outlays = transform_series(df, 5).dropna()*100
pct_chg_fed_outlays.plot()
plt.show()


#demean and checking for stationarity
print("ADF Test Result: ", adfuller(pct_chg_fed_outlays, regression="c"))
print("ADF Test Result: ", adfuller(transform_series(pct_chg_fed_outlays, 5).dropna(), regression="c"))
plot_acf_pacf(pct_chg_fed_outlays)
plt.show()


#looks like a garch(1, 1) is suitable
model = arch_model(pct_chg_fed_outlays['pct_chg'], mean = 'AR', lags = 1, vol='Garch', p=1, q=1)
fit = model.fit()
# print(fit.summary())

last_month = pct_chg_fed_outlays.index[-1]+ pd.offsets.MonthBegin(1)

#prediction
pred = fit.forecast(horizon=4-int(last_month.month)%4).mean.iloc[-1].values

new_dates = pd.date_range(start = last_month , periods = 4-int(last_month.month)%4, freq='MS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred = pd.concat([pct_chg_fed_outlays['pct_chg'], new_df])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_chg_pce(date = "2020-01-01"):
    return quarterly_pct_chage