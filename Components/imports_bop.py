from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-01-01"

df = get_most_recent_series_of_date("BOPTIMP", given_date, fred)
df = df[df.index<=pd.to_datetime("2006-06-01")]

#df = get_most_recent_series_of_date("TLPBLCONS", "2020-01-01", fred)

pct_chg_imports_bop = transform_series(df, 5).dropna()*100
pct_chg_imports_bop.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_imports_bop, regression="c"))
print("ADF Test Result: ", adfuller(transform_series(pct_chg_imports_bop, 5).dropna(), regression="c"))
plot_acf_pacf(pct_chg_imports_bop)
plt.show()