from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)

df = difference_df(df, 1)
diff_df = df['Diff_Value']

# Plotting ACF and PACF of the first diff in pct chg in GDP
# diff_df.plot()
# plt.show()
# plot_acf_pacf(diff_df)
# plot_acf_pacf(diff_df**2)
# Suggesting that a GARCH model might be suitable, can consider, q = [0, 1, 2] and p = [1, 2, 3, 4], which may be overkill may want to consider lags up to 1


train, test = train_test_split(diff_df, test_size=50, shuffle=False)
# print(train.size)
# 239 obs for train and validation

# CV for p and q where p = [1, 2, 3, 4] and q = [0, 1, 2] and lags up to 1
# array = np.zeros(24)

# rmse_cv = []

# for p in [1, 2, 3, 4]:
#     for q in [0, 1, 2]:
#         for lags in [0, 1]:
#             pred = []
#             for index in range(1, 51):
#                 train = train.iloc[:239-index-1]   
#                 model = arch_model(train, vol='Garch', p=p, q=q, mean = 'AR', lags = lags).fit(disp = False)  
#                 pred.append(model.forecast(horizon=1).mean.iloc[-1].values[0])  
#             pred.reverse() 
#             test_recon = train.iloc[-50:].cumsum()
#             pred = pd.Series(pred, index= test_recon.index)  
#             pred_recon = pred.cumsum()
#             rmse_cv.append(mean_squared_error(pred_recon, test_recon, squared=False))


#RMSE of CV
# print(rmse_cv)
# no lag looks superior, would produce the same results as prevailing mean

#Eval on test set
# pred = []
# for index in range(1, 51):
#     test_obs = diff_df.iloc[-index]
#     train = diff_df.iloc[:290-1-index]
#     train_lag = train.shift(1)
#     model = arch_model(train, vol='Garch', p=4, q=0, mean = 'zero').fit(disp = False)
#     pred.append(model.forecast(horizon=1).mean.iloc[-1].values[0])


# pred.reverse()
# print(pred)
# pred_recon = pd.Series(pred, index= test.index).cumsum()
# test_recon = test.cumsum()

# #plotting of resid
# fig, ax = plt.subplots()
# ax.plot(pred_recon)
# ax.plot(test_recon)
# plt.show()

# #evaluation
# rmse = mean_squared_error(test, pred, squared=False)
# print(f'Root Mean Squared Error: {rmse}')

# mae = mean_absolute_error(test, pred)
# print(f'Mean Absolute Error: {mae}')

# directional_pred = ((pred * test)>0).sum()/test.size
# print(f'Directional Accuracy: {directional_pred}')

# #Future Prediction
# last_quart = df.index[-1]+ pd.offsets.QuarterBegin(1)

# pred = model.forecast(horizon=2).mean.iloc[-1].values

# new_dates = pd.date_range(start = last_quart , periods = 2, freq='MS')
# new_df = pd.Series(pred, index=new_dates)
# pct_chg_pred_gdp = pd.concat([df['pct_chg'], new_df])



