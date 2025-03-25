from consumption import *
from nett_exports import *


fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
df['lag_GDP'] = df.pct_chg.shift()
# df.plot()
# plt.show()

ne = quart_pct_chg_ne()
pce = quart_pct_chg_pce()

compiled = pd.concat([ne, pce, df.lag_GDP, df.pct_chg], axis = 1).dropna()
compiled.columns = ['Nett_Exports', 'PCE','lag_GDP' ,'GDP']

X = compiled.iloc[:, :3]
y = compiled.GDP

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=50)

def load_data():
    return X_train, X_test, y_train, y_test