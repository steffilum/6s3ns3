from .imports import *
# differences a dataframe by adding a lag
# takes in a df with a time index and value
# returns a df with time index, value and lag value but w 1 less obs
def difference_df(df):
    df = df.to_frame()
    df = df.rename(columns = {0: "Value"})
    df["Lagged Value"] = df["Value"].diff()
    lagged_value = df["Lagged Value"].dropna()
    return lagged_value

#gets the most recent df of a series
# takes in the series key and end date
#returns a series whos index is date and value
def get_most_recent_df_of_date(series_key, end_date, fred):
    df = fred.get_series_as_of_date(series_key, end_date).drop_duplicates(subset = ["date"], keep = "last")
    df = pd.Series(df["value"].to_list(), index = df["date"].to_list())
    df = df.dropna()
    df = df.astype("float")
    return df

#returns the best aic given a stationary time series to use in an ar model
#takes in a df
#returns the best lags to use in an ar model
def best_aic(df, max_lag_to_try):
    best_aic = float("inf")
    best_lag = None

    for lag in range(1, max_lag_to_try):  
        model = AutoReg(df, lags=lag).fit()
        aic = model.aic
    
        if aic < best_aic:
            best_aic = aic
            best_lag = lag
    return best_lag