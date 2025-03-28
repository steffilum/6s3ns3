from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-01-01"

df = get_most_recent_series_of_date("BOPTIMP", given_date, fred)
df = df[df.index<=pd.to_datetime("2006-06-01")]

pct_chg_imports_bop = transform_series(df, 5).dropna()*100
pct_chg_imports_bop.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_imports_bop, regression="c"))
print("ADF Test Result: ", adfuller(transform_series(pct_chg_imports_bop, 5).dropna(), regression="c"))
plot_acf_pacf(pct_chg_imports_bop)
plt.show()

# best_arma(pct_chg_imports_bop, trend='c', test_size=10, start_p= 0, start_q=0, max_p=5, max_q=5)
# best arma p=3, q=4, gridsearch: p=3, q=3

model = ARIMA(pct_chg_imports_bop, order=(3, 0, 4), trend = 'c', freq = 'MS')
model = model.fit(start_params = np.full(3+4+1+1, .01))

plt.plot(model.resid)
plt.show()

start_date_pred = pct_chg_imports_bop.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time

#prediction
pred = model.predict(start = start_date_pred, end = end_date_pred)

pct_chg_pred = pd.concat([pct_chg_imports_bop, pred])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()