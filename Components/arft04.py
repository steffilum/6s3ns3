from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2020-03-01"

df = get_most_recent_series_of_date("GDP", given_date, fred)
df = pct_chg(df)

df = df.pct_chg

_, test = train_test_split(df, test_size=50, shuffle=False)

df.index = pd.to_datetime(df.index).to_period('Q')

print(df.shape)

pred = []

for index in range(1, 51):
    train = df.iloc[:291-index]
    model = AutoReg(train, lags = 4, trend = 'ct').fit()
    pred.append(model.predict(start = 291-index, end = 291-index))

# print(model.params)

pred.reverse()
pred = pd.concat(pred)
pred.index = pred.index.to_timestamp()
print(pred)
print(test)

eval(test, pred, plot=True)

