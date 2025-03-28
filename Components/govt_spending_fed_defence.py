from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-01-01"

df = get_most_recent_series_of_date("FDEFX", given_date, fred)
df = df[df.index<=pd.to_datetime("2006-06-01")]
df = df[df.index >= pd.to_datetime("1953-01-01")]
print(df)

#transform series
pct_chg_fed_defence = transform_series(df, 5).dropna()*100
# outlier in 1951 due to Korean War, to keep data from 1953 onwards

pct_chg_fed_defence.plot()
plt.show()


#demean and checking for stationarity
print("ADF Test Result: ", adfuller(pct_chg_fed_defence, regression="c"))
print("ADF Test Result: ", adfuller(transform_series(pct_chg_fed_defence, 5).dropna(), regression="c"))
plot_acf_pacf(pct_chg_fed_defence)
plt.show()


best_arma(pct_chg_fed_defence, trend='c', test_size=10, start_p= 0, start_q=0, max_p=5, max_q=5, freq="QS")
model = ARIMA(pct_chg_fed_defence, order=(4, 0, 5), trend = 'c', freq = 'QS').fit()
fig, ax = plt.subplots()
ax.plot(model.fittedvalues)
ax.plot(pct_chg_fed_defence)
plt.show()
last_month = pct_chg_fed_defence.index[-1]+ pd.offsets.MonthBegin(1)


start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').start_time + pd.offsets.MonthBegin(-1)

#prediction
pred = model.predict(horizon=4-int(last_month.month)%4).mean.iloc[-1].values

new_dates = pd.date_range(start = last_month , periods = 4-int(last_month.month)%4, freq='MS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred = pd.concat([pct_chg_fed_defence['pct_chg'], new_df])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_chg_pce(date = "2020-01-01"):
    return quarterly_pct_chage