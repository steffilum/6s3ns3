from data_load import *

X, y = load_data_bridge()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=50, shuffle = False)

X = sm.add_constant(X)

# print(X.shape)

vif_data = pd.DataFrame()
vif_data["Feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# Evaluation on test set
pred = []
for index in range(1, 51):
    X_train = X.iloc[:-index, :]
    y_train = y.iloc[:-index]
    X_test = X.iloc[-index, :]
    model = sm.OLS(y_train, X_train).fit()
    pred.append(model.predict(X_test)[0])

pred.reverse()

y_test = y.iloc[-50:]
pred = pd.Series(pred, index = y_test.index)

#evaluation
eval(pred, y_test)

model = sm.OLS(y, X).fit()
print(model.summary())
