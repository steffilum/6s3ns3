from data_load import *

X, y= load_data_rf()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=50, shuffle = False)

best_rmse = 0
best_trees = 0
rmse = []
for trees in range(10, 1000, 10):
    rmse.append(0)
    for index in range(1, 10):
        X_cv = X_train.iloc[:-index-1, :]
        y_cv = y_train.iloc[:-index-1]
        X_validate = X_train.iloc[-index, :].values.reshape(1, -1) 
        y_validate = y_train.iloc[-index]
        regressor = RandomForestRegressor(n_estimators=trees, n_jobs = 4) 
        regressor.fit(X_cv, y_cv)
        prediction = regressor.predict(X_validate)
        rmse[-1] += (y_validate - prediction)**2
plt.plot(rmse)
plt.show()

# best at 1240

# Evaluation on test set
pred = []
for index in range(1, 51):
    X_train = X.iloc[:-index-1, :]
    y_train = y.iloc[:-index-1]
    X_validate = X.iloc[-index, :].values.reshape(1, -1) 
    regressor = RandomForestRegressor(n_estimators=1000, n_jobs = 4) 
    regressor.fit(X_train, y_train)
    prediction = regressor.predict(X_validate)
    pred.append(prediction)

pred.reverse()
pred = pd.Series(pred, index = y_test.index)

#evaluation
eval(pred, y_test)