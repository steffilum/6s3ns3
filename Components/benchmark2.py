from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
# df.plot()
# (df**2).plot()
# plt.show()

# Plotting ACF and PACF of the closing value time series
# plot_acf_pacf(df.pct_chg)
# plot_acf_pacf(df.pct_chg**2)
# Suggesting that a GARCH model might be suitable

train, test = train_test_split(df.pct_chg, test_size=50, shuffle=False)
# print(train.size)
# 240 obs for train and validation

# CV for p and q where p = [0, 1, 2] and q = [0, 1, 2]
array = np.zeros(6)

# for index in range(1, 51):
#     validation = train.iloc[-index]
#     train = train.iloc[:239-index]
#     for p in [1, 2]:
#         for q in [0, 1, 2]:
#             model = arch_model(train, vol='Garch', p=p, q=q).fit(disp = False)
#             array[q*2+p-1] += (model.forecast(horizon=1).mean.iloc[-1].values[0]-validation)**2

# print(array)
# Garch (1, 1) looks the best
pred = []
for index in range(1, 51):
    test_obs = df.pct_chg.iloc[-index]
    train = df.pct_chg.iloc[:290-1-index]
    train_lag = train.shift(1)
    model = arch_model(train, vol='Garch', p=1, q=1, mean = 'AR', lags = 2).fit(disp = False)
    pred.append(model.forecast(horizon=1).mean.iloc[-1].values[0])

pred.reverse()
pred = pd.Series(pred, index= test.index)
print(pred)

fig, ax = plt.subplots()
ax.plot(pred)
ax.plot(test)
plt.show()

#evaluation
rmse = mean_squared_error(test, pred, squared=False)
print(f'Root Mean Squared Error: {rmse}')

mae = mean_absolute_error(test, pred)
print(f'Mean Absolute Error: {mae}')

directional_pred = ((pred * test)>0).sum()/test.size
print(f'Directional Accuracy: {directional_pred}')

#Future Prediction
last_quart = df.index[-1]+ pd.offsets.QuarterBegin(1)

pred = model.forecast(horizon=2).mean.iloc[-1].values

new_dates = pd.date_range(start = last_quart , periods = 2, freq='MS')
new_df = pd.Series(pred, index=new_dates)
pct_chg_pred_gdp = pd.concat([df['pct_chg'], new_df])



