from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)

df = df.pct_chg

_, test = train_test_split(df, test_size=50, shuffle=False)

df = df.reset_index()  
df = df.rename(columns={'index': 'ds', 'pct_chg': 'y'})  
# print(df.head())

print(df.shape)

pred = []

for index in range(1, 51):
    train = df.iloc[:291-index]
    print(train.tail())
    model = Prophet()
    model.fit(train)
    future = model.make_future_dataframe(periods=1, freq='Q')
    forecast = model.predict(future).iloc[-1, :]
    array = forecast.iloc[[0,-1]]
    pred.append(array)

pred = pd.DataFrame(pred)
pred['ds'] = pd.to_datetime(pred['ds'])
pred = pred.set_index('ds')
pred.index = pred.index + pd.DateOffset(days=1)
print(pred)
pred.sort_index(inplace=True)

eval(test, pred, plot=True)

