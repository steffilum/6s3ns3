from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_series_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
# df.plot(y = "pct_chg")
# plt.show()

df = df.pct_chg
_, test = train_test_split(df, test_size=50, shuffle=False)

pred = []

for index in range(1, 51):
    pred.append(df.iloc[:-index].mean())

pred.reverse()
pred = pd.Series(pred, index = test.index)

#evaluation
eval(pred, test, plot=True)