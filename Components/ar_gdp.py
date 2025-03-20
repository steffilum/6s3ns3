from fredapi import Fred
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.ar_model import AutoReg

fred = Fred(api_key = '084a38e9d6fd82146cf89b8c30eba224')


def get_prediction(series_key, end_date, n):
    df = fred.get_series_as_of_date(series_key, end_date).drop_duplicates(subset = ["date"], keep = "last")
    df = pd.Series(df["value"].to_list(), index = df["date"].to_list())
    df = df.dropna()
    df = df.astype("float")
    df = np.log(df)
    
    df = df.to_frame()
    df = df.rename(columns = {0: "Value"})
    df["Lagged Value"] = df["Value"].diff()
    lagged_value = df["Lagged Value"].dropna()
    
    df.plot(y = "Lagged Value")
    plt.show()
    
    print("ADF Test Result: ", adfuller(lagged_value))
    
    best_aic = float("inf")
    best_lag = None

    for lag in range(1, 11):  # Try lags from 1 to 11
        model = AutoReg(lagged_value, lags=lag).fit()
        aic = model.aic
    
        if aic < best_aic:
            best_aic = aic
            best_lag = lag
            
    print("Optimal Lag Value: ", best_lag)
            
    model = AutoReg(lagged_value, lags = best_lag).fit()
    prediction = model.predict(start = len(lagged_value), end = len(lagged_value) + n)
    return prediction

print(get_prediction("GDP", "2020-01-01", 2))