from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

#df = get_most_recent_series_of_date("TLPBLCONS", "2006-01-01", fred)
given_date = "2020-01-01"

df = get_most_recent_series_of_date("TLPBLCONS", given_date, fred)
df = df[df.index<=pd.to_datetime("2006-06-01")]

## need to double check the correct transformation for this
pct_chg_govt_construction = transform_series(df, 5).dropna()*100
pct_chg_govt_construction.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_govt_construction, regression="c"))
print("ADF Test Result: ", adfuller(transform_series(pct_chg_govt_construction, 5).dropna(), regression="c"))
plot_acf_pacf(pct_chg_govt_construction)
plt.show()

best_arma(pct_chg_govt_construction, trend='c', test_size=10, start_p= 0, start_q=0, max_p=5, max_q=5)
model = ARIMA(pct_chg_govt_construction, order=(0, 0, 0), trend = 'c', freq = 'MS').fit()
fig, ax = plt.subplots()
ax.plot(model.fittedvalues)
ax.plot(pct_chg_govt_construction)
plt.show()
last_month = pct_chg_govt_construction.index[-1]+ pd.offsets.MonthBegin(1)