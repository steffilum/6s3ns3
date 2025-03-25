from data_load import *

X, y = load_data()

X = compiled.iloc[:, :-1]
X = sm.add_constant(X)
y = compiled.GDP
# print(X.shape)

# Evaluation on test set
pred = []
for index in range(1, 51):
    y_test = y.iloc[-index]
    X_train = X.iloc[:-index, :]
    y_train = y.iloc[:-index]
    X_test = X.iloc[-index, :]
    model = sm.OLS(y_train, X_train).fit()
    pred.append(model.predict(X_test)[0])

pred.reverse()

y_test = y.iloc[-50:]
pred = pd.Series(pred, index = y_test.index)

#evaluation
rmse = mean_squared_error(y_test, pred, squared=False)
print(f'Root Mean Squared Error: {rmse}')

mae = mean_absolute_error(y_test, pred)
print(f'Mean Absolute Error: {mae}')

directional_pred = ((pred * y_test)>0).sum()/y_test.size
print(f'Directional Accuracy: {directional_pred}')

new_X = np.array([1, ne.values[-1], pce.values[-1], df.lag_GDP[-1]])

predictions = model.predict(new_X)

print("Predicted values:", predictions)
