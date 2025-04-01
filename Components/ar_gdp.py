from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))


def get_prediction(series_key, end_date, n, fred):
    df = get_most_recent_series_of_date(series_key, end_date, fred)
    df = np.log(df)
    
    lagged_value = difference_df(df)
    
    lagged_value.plot(y = "Lagged Value")
    plt.show()
    
    print("ADF Test Result: ", adfuller(lagged_value))
    
    best_lag = best_aic(lagged_value, 11)
            
    print("Optimal Lag Value: ", best_lag)
            
    model = AutoReg(lagged_value, lags = best_lag).fit()
    prediction = model.predict(start = len(lagged_value), end = len(lagged_value) + n)
    return prediction

print(get_prediction("GDP", "2020-01-01", 2, fred))

