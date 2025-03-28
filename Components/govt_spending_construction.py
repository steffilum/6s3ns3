from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("TLPBLCONS", "2020-01-01", fred)


## need to double check the correct transformation for this
pct_chg_govt_construction = transform_series(df, 5).dropna()*100