from data_load import *

X_train, X_test, y_train, y_test = load_data()
X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=50)

# best_rmse = 0
# best_trees = 0
# rmse = []
# for trees in range(0, 1300, 10):
#     regressor = RandomForestRegressor(n_estimators=trees, n_jobs = 4) 

#     regressor.fit(X_train, y_train)

#     predictions = regressor.predict(X_validation)

#     rmse.append(mean_squared_error(y_validation, predictions, squared=False))

# plt.plot(rmse)
# plt.show()

#best at 1240

# eval
# regressor = RandomForestRegressor(n_estimators=1240, n_jobs=4).fit(X_test, y_test)
# pred = regressor.predict(X_validation)
# eval(pred, y_test)