from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("NETEXP", "2020-01-01", fred)

pct_chg_ne = df.pct_change()*100

# pct_chg_ne.plot()
# plt.show()

#showing a large spike in the data during 1973 due to the oapec making us goods very expensive thus may choose to cut off the data from 1974 and 1980s due to latin 
#debt crises
filtered = pct_chg_ne[pct_chg_ne.index>'1983-01-01']
filtered.plot()
plt.show()

#check if stationary

# last_month = pct_chg_pce.index[-1]+ pd.offsets.MonthBegin(1)
# new_dates = pd.date_range(start = last_month , periods = 4-int(last_month.month)%4, freq='MS')
# new_df = pd.Series([pred]*(4-last_month.month%4), index=new_dates)
# pct_chg_pred = pd.concat([pct_chg_pce['pct_chg'], new_df])

# quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

# def quart_pct_chg_pce():
#     return quarterly_pct_chage