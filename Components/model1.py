from data_load import *

X, y = load_data()

X = compiled.iloc[:, :3]
y = compiled.GDP

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())

new_X = np.array([1, ne.values[-1], pce.values[-1], df.lag_GDP[-1]])

predictions = model.predict(new_X)

print("Predicted values:", predictions)
