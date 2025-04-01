from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)
print(df)