from consumption import *
from nett_exports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)


# print(quart_pct_chg_ne())
# print(quart_pct_chg_pce())
# print(df)

ne = quart_pct_chg_ne()
pce = quart_pct_chg_pce()

compiled = pd.concat([ne, pce, df.pct_chg], axis = 1).dropna()
compiled.columns = ['Nett_Exports', 'PCE', 'GDP']

X = compiled.iloc[:, :2]
y = compiled.GDP

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())

new_X = np.array([1, ne.values[-1], pce.values[-1]])

predictions = model.predict(new_X)

print("Predicted values:", predictions)
