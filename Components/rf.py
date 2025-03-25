from data_load import *

X, y = load_data()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.05, random_state=2025, shuffle=False)

best_rmse = 0
best_trees = 0
rmse = []
r2 = []
for trees in range(300, 2000, 100):
    regressor = RandomForestRegressor(n_estimators=trees, n_jobs = 4, random_state=2025) 

    regressor.fit(X_train, y_train)


    predictions = regressor.predict(X_test)

    rmse.append(mean_squared_error(y_test, predictions)**.5)
    r2.append(r2_score(y_test, predictions))

    # mse = mean_squared_error(y_test, predictions)
    # print(f'Mean Squared Error: {mse}')

    # r2 = r2_score(y_test, predictions)
    # print(f'R-squared: {r2}')

plt.plot(rmse)
plt.plot(r2)
plt.show()
# y_pred = regressor.predict(X_train)
# resid = y_train-y_pred

# plt.scatter(X_train.lag_GDP, resid)
# plt.show()