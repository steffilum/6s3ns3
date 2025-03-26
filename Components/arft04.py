from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)

df = df.pct_chg

_, test = train_test_split(df, test_size=50, shuffle=False)

df.index = pd.to_datetime(df.index).to_period('Q')

# print(df.shape)

pred = []

for index in range(1, 51):
    train = df.iloc[:290-index-1]
    model = AutoReg(train, lags = 4, trend = 'ct').fit()
    pred.append(model.predict(start = 290-index, end = 290-index))

# print(model.params)

pred.reverse()
pred = pd.concat(pred)
pred.index = pred.index.to_timestamp()

eval(test, pred, False)

