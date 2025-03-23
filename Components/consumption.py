from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("PCE", "2020-01-01", fred)

pct_chg_pce = pct_chg(df)

#demean
pct_chg_pce['demean_pct_chg'] = pct_chg_pce.pct_chg-pct_chg_pce.pct_chg.mean()
# plot_acf_pacf(pct_chg_pce['demean_pct_chg'] )
# plt.show()

#After demeaning looks like whit noise that centers around the mean

#prediction would be the mean
pred = pct_chg_pce.pct_chg.mean()

last_month = pct_chg_pce.index[-1]+ pd.offsets.MonthBegin(1)
new_dates = pd.date_range(start = last_month , periods = 4-int(last_month.month)%4, freq='MS')
new_df = pd.Series([pred]*(4-last_month.month%4), index=new_dates)
pct_chg_pred = pd.concat([pct_chg_pce['pct_chg'], new_df])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_chg_pce():
    return quarterly_pct_chage