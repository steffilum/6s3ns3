from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("NETEXP", "2020-01-01", fred)

pct_chg_ne = df.pct_change()*100

# pct_chg_ne.plot()
# plt.show()

#showing a large spike in the data during 1973 due to the oapec making us goods very expensive thus may choose to cut off the data from 1974 and 1980s due to latin 
#debt crises
filtered = pct_chg_ne[pct_chg_ne.index>'1984-01-01']
# filtered.plot()
# plt.show()


#check if stationary for after 1983
# print("ADF Test Result: ", adfuller(filtered))

#testing for garch model
# filtered.plot()
# (filtered**2).plot()
# plt.show()

model = arch_model(filtered, mean = 'AR', lags = 1, vol='Garch', p=1, q=1)
fit = model.fit()
# print(fit.summary())

last_quart = filtered.index[-1]+ pd.offsets.QuarterBegin(1)

#prediction
pred = fit.forecast(horizon=2).mean.iloc[-1].values

new_dates = pd.date_range(start = last_quart, periods = 2, freq='QS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred_ne = pd.concat([pct_chg_ne, new_df])

def quart_pct_chg_ne(date = "2020-01-01"):
    return pct_chg_pred_ne