from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-01-01"

df = get_most_recent_series_of_date("PCE", given_date, fred)

pct_chg_pce = transform_series(df, 5).dropna()*100
# pct_chg_pce.plot()
# plt.show()
# Visually the data looks like it was going up then drops after 1975
pct_chg_pce = pct_chg_pce[pct_chg_pce.index>pd.to_datetime("1975-01-01")]
# pct_chg_pce.plot()
# plt.show()
# checking for stationarity
print("ADF Test Result: ", adfuller(pct_chg_pce, regression='c'))
# plot_acf_pacf(pct_chg_pce)
# plt.show()

#gridsearch chosen base on pcf and acf
best_arma(pct_chg_pce, trend='c', test_size=10, start_p= 0, start_q=0, max_p=5, max_q=5)
model = ARIMA(pct_chg_pce, order=(0, 0, 0), trend = 'c', freq = 'MS').fit()
fig, ax = plt.subplots()
ax.plot(model.fittedvalues)
ax.plot(pct_chg_pce)
plt.show()
# pred = model.get_forecast(steps = 1).predicted_mean
# print(pred)

start_date_pred = pct_chg_pce.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').start_time + pd.offsets.MonthBegin(-1)

#prediction
pred = model.predict(horizon=4-int(last_month.month)%4).mean.iloc[-1].values

new_dates = pd.date_range(start = last_month , periods = 4-int(last_month.month)%4, freq='MS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred = pd.concat([pct_chg_pce['pct_chg'], new_df])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_chg_pce(date = "2020-01-01"):
    return quarterly_pct_chage