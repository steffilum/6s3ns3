from consumption import *
from nett_exports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)

print(quart_pct_chg_ne())
print(quart_pct_chg_pce())
print(df)
