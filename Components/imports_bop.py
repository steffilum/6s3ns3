from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("BOPTIMP", "2020-01-01", fred)

pct_chg_imports_bop = transform_series(df, 5).dropna()*100