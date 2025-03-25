from .imports import *
# differences a dataframe by adding a lag
# takes in a series with a time index and value
# returns a df with time index, value and lag value but w 1 less obs
def difference_df(df, col = 0):
    if isinstance(df, pd.Series):
        df = df.to_frame()
        df = df.rename(columns = {df.columns[0]: "Value"})
        df["Diff_Value"] = df["Value"].diff()
        df = df.dropna()
        return df
    else:
        df["Diff_Value"] = df.iloc[:, col].diff()
        df = df.dropna()
        return df

#gets the most recent df of a series
# takes in the series key and end date
#returns a series whos index is date and value
def get_most_recent_df_of_date(series_key, end_date, fred):
    df = fred.get_series_as_of_date(series_key, end_date).drop_duplicates(subset = ["date"], keep = "last")
    df = pd.Series(df["value"].to_list(), index = df["date"].to_list())
    df.index = pd.to_datetime(df.index)
    df = df.dropna()
    df = df.astype("float")
    return df

#returns the best aic given a stationary time series to use in an ar model
#takes in a df
#returns the best lags to use in an ar model
def best_aic(df, max_lag_to_try):
    best_aic = float("inf")
    best_lag = None

    for lag in range(0, max_lag_to_try+1):  
        model = AutoReg(df, lags=lag).fit()
        aic = model.aic
    
        if aic < best_aic:
            best_aic = aic
            best_lag = lag
    return best_lag

# takes the rough percent change in a df
# takes in a df with a time index and value
# returns a series with time index, value and lag value but w 1 less obs
def pct_chg(df, col = 0):
    if isinstance(df, pd.Series):
        df = np.log(df)
        df = df.to_frame()
        df = df.rename(columns = {0: "Value"})
        df["pct_chg"] = df["Value"].diff()*100
        df = df.dropna()
        return df
    else:
        df["pct_chg"] = np.log(df.iloc[:, col]).diff()*100
        df= df.dropna()
        return df
    
# Function to plot ACF and PACF
#takes in a time series then plots the acf and pacf
def plot_acf_pacf(timeseries):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    plot_acf(timeseries, ax=ax1, lags=75)
    plot_pacf(timeseries, ax=ax2, lags=75)
    plt.show()

# prints various eval metrics
#takes in test and pred, does not return, prints out required metrics
def eval(test, pred):
    rmse = mean_squared_error(test, pred, squared=False)
    print(f'Root Mean Squared Error: {rmse}')

    mae = mean_absolute_error(test, pred)
    print(f'Mean Absolute Error: {mae}')

    directional_pred = ((pred * test)>0).sum()/test.size
    print(f'Directional Accuracy: {directional_pred}')