from package_imports import *
from data_load import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

date = pd.to_datetime(given_date)

# while True:
#     date = date - pd.offsets.MonthBegin(1)
#     df = get_most_recent_series_of_date("UNRATE", date, fred)
#     if df.empty:
#         print(date)
#         break
#     else: print(f'{date} OK')

# df = get_most_recent_series_of_date("IPBUSEQ", date, fred)
# print(df)
# X, y = load_data_midas(given_date=given_date)
# print(X.Import_m1)
# for i in X.values:
#     print(i)

# df = get_most_recent_series_of_date("BOPTIMP", "2010-05-01", fred)
# pct_chg_fed_defence = transform_series(df, 5).dropna()*100
# pct_chg_fed_defence = pct_chg_fed_defence[pct_chg_fed_defence.index<pd.to_datetime(given_date) - pd.offsets.MonthBegin(1)]
# print(pct_chg_fed_defence.tail(20))

# print(quart_pct_chg_biz_equip("2001-01-01", 'M').tail(30))
print(load_data_midas(given_date))