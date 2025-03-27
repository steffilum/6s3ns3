from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("MTSO133FMS", "2020-01-01", fred)

govt_chg_pce = pct_chg(df)

#demean and checking for stationarity
govt_chg_pce['demean_pct_chg'] = govt_chg_pce.pct_chg-govt_chg_pce.pct_chg.mean()
# print("ADF Test Result: ", adfuller(difference_df(pct_chg_pce['demean_pct_chg'])['Diff_Value']))
# plot_acf_pacf(pct_chg_pce['demean_pct_chg'] )
# plot_acf_pacf(pct_chg_pce['demean_pct_chg']**2)
# plt.show()

#looks like a garch(1, 1) is suitable
model = arch_model(govt_chg_pce['pct_chg'], mean = 'AR', lags = 1, vol='Garch', p=1, q=1)
fit = model.fit()
# print(fit.summary())

last_month = govt_chg_pce.index[-1]+ pd.offsets.MonthBegin(1)

#prediction
pred = fit.forecast(horizon=4-int(last_month.month)%4).mean.iloc[-1].values

new_dates = pd.date_range(start = last_month , periods = 4-int(last_month.month)%4, freq='MS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred = pd.concat([govt_chg_pce['pct_chg'], new_df])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_chg_pce(date = "2020-01-01"):
    return quarterly_pct_chage