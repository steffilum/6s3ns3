from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("PCE", "2020-01-01", fred)

pct_chg_pce = transform_series(df, 5).dropna()*100
pct_chg_pce.plot()
plt.show()

# checking for stationarity
print("ADF Test Result: ", adfuller(pct_chg_pce, regression='c'))
print("ADF Test Result: ", adfuller(transform_series(pct_chg_pce, 5).dropna(), regression='c'))
plot_acf_pacf(pct_chg_pce)
plt.show()

best_arma(pct_chg_pce, trend='ct', test_size=1, start_p= 8, start_q=8, max_p=10, max_q=10)
# model = ARIMA(pct_chg_pce, order=(11, 0, 23), trend = 'ct', freq = 'MS').fit()
# pred = model.get_forecast(steps = 1).predicted_mean
# print(pred)


#looks like a garch(3, 9) is suitable with 8 lags from the acf and pacf
# model = arch_model(pct_chg_pce, mean = 'AR', lags = lags, vol='Garch', p=3, q=9)
# fit = model.fit()
# print(fit.summary())

last_month = pct_chg_pce.index[-1]+ pd.offsets.MonthBegin(1)

#prediction
pred = fit.forecast(horizon=4-int(last_month.month)%4).mean.iloc[-1].values

new_dates = pd.date_range(start = last_month , periods = 4-int(last_month.month)%4, freq='MS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred = pd.concat([pct_chg_pce['pct_chg'], new_df])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_chg_pce(date = "2020-01-01"):
    return quarterly_pct_chage