from consumption import *
from nett_exports import *

fred = Fred(api_key = os.getenv("API_KEY"))

print(fred.get_series_as_of_date("GDP", "2020-01-01"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
# df.plot()
# plt.show()

ne = quart_pct_chg_ne()
pce = quart_pct_chg_pce()

compiled = pd.concat([ne, pce, df.pct_chg], axis = 1).dropna()
compiled.columns = ['Nett_Exports', 'PCE', 'GDP']

X = compiled.iloc[:, :2]
y = compiled.GDP


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.05, random_state=2025, shuffle=False)


regressor = RandomForestRegressor(n_estimators=1000, n_jobs = 4, random_state=2025) 

regressor.fit(X_train, y_train)


predictions = regressor.predict(X_test)

mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

r2 = r2_score(y_test, predictions)
print(f'R-squared: {r2}')
