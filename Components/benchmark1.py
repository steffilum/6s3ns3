from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
# df.plot(y = "pct_chg")
# plt.show()

train, test = train_test_split(df.pct_chg, test_size=50, shuffle=False)
print(train.size)

#prediction using mean = 1.5418%
print(train.mean())
pred = pd.Series(1.5418, index = test.index)
# print(pred)

#evaluation
rmse = mean_squared_error(test, pred, squared=False)
print(f'Root Mean Squared Error: {rmse}')

mae = mean_absolute_error(test, pred)
print(f'Mean Absolute Error: {mae}')

directional_pred = ((pred * test)>0).sum()/test.size
print(f'Directional Accuracy: {directional_pred}')