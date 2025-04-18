from .imports import *

def difference_df(df, col = 0):
    '''
    Differences a time series by adding a lag. 

    Parameters:
    ______________________________
    df: pandas.Series or pandas.DataFrame
        Time series.

    col: int.
        Zero-based index of the dataframe column corresponding to the time series.

    Returns: 
    ______________________________
    pandas.DataFrame
        The input Series or DataFrame object with time index, an additional column of differenced values and 1 less observation. 
    '''
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

def get_most_recent_series_of_date(series_key, end_date, fred):
    '''
    Retrieves FRED data on an economic indicator up till the latest entry as of a certain date.

    Parameters:
    ______________________________
    series_key: string
        The key of the economic indicator in FRED's database: https://fred.stlouisfed.org/release?rid=205.

    end_date: string
        The date in YYYY-MM-DD format. 

    fred: fredapi 
        The fredapi object to pull FRED data from.

    Returns: 
    ______________________________
    pandas.Series
        The values of the input economic indicator, with a date index.
    '''    
    df = fred.get_series_as_of_date(series_key, end_date).drop_duplicates(subset = ["date"], keep = "last")
    df = pd.Series(df["value"].to_list(), index = df["date"].to_list())
    df.index = pd.to_datetime(df.index)
    df = df.dropna()
    df = df.astype("float")
    return df
    
def best_arma(df, start_p = 0, start_q = 0, max_p = 5, max_q = 5, test_size = 50, trend = None, freq = 'MS', exog = None, seasonal_order = (0, 0, 0, 0)):
    '''
    Chooses the best hyperparameters of the ARMA model for a time series, using out-of-sample forecasting.

    Parameters:
    ______________________________
    df: pandas.Series or pandas.DataFrame
        The stationary time series.

    start_p: int
        The lower bound of the GridSearch for the p parameter (lag order) of the ARMA model.

    start_q: int
        The lower bound of the GridSearch for the q parameter (moving average order) of the ARMA model.

    max_p: int
        The upper bound of the GridSearch for the p parameter (lag order) of the ARMA model.

    max_q: int
        The upper bound of the GridSearch for the q parameter (moving average order) of the ARMA model. 

    test_size: int
        The size of the test sample for hyperparameter tuning.
        
    trend: string
        Deterministic trend of the time series. 
    
    freq: string
        Frequency of the time-series. 

    exog: pandas.Series or array-like
        Exogenous regressors (if any).

    seasonal_order: tuple
        The (P,D,Q,s) order of the seasonal component of the ARMA model, representing the lag order, difference (default 0), moving average order and periodicity respectively. 

    Returns: 
    ______________________________
    p: int
        Optimal lag order for the ARMA model of the input time series.

    q: int
        Optimal moving average order for the ARMA model of the input time series.
    '''

    df = df.asfreq(freq)

    p_range = range(start_p, max_p+1) 
    q_range = range(start_q, max_q+1)  

    results = np.full((max_p-start_p+1, max_q-start_q+1),np.inf)

    for index in range(1, test_size+1):
        train = df.iloc[:-index-1]
        test = df.iloc[-index]
        for p in p_range:
            for q in q_range:
                
                try:
                    model = ARIMA(train, order=(p, 0, q), trend = trend, freq=freq, enforce_stationarity=False, enforce_invertibility=False, seasonal_order=seasonal_order)
                    model = model.fit(method_kwargs={'maxiter':100})
                    pred = model.get_forecast(steps = 1).predicted_mean
                    if results[p-start_p-1][q-start_q-1] == np.inf:
                        results[p-start_p-1][q-start_q-1] = 0
                    results[p-start_p-1][q-start_q-1] += (pred-test)**2                
                except TypeError:
                    print(f'Try other params for{(p, 0, q)}')
    print(results)
    flat_index = np.argmin(results)
    p, q = np.unravel_index(flat_index, results.shape)

    print(f'Best ARIMA model order: p={p+start_p} and q={q+start_q}')
    return p, q

def pct_chg(df, col = 0):
    '''
    Gives a rough percentage change between consecutive values in a time series. 

    Parameters:
    ______________________________
    df: pandas.Series or pandas.DataFrame
        Time series.

    col: int
        Zero-based index of the dataframe column corresponding to the time series.

    Returns: 
    ______________________________
    pandas.DataFrame
        The input Series or DataFrame object with time index, an additional column of percentage change values and 1 less observation. 
    '''
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
    
def plot_acf_pacf(timeseries):
    '''
    Plots the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) for a time series.

    Parameters:
    ______________________________
    timeseries: pandas.Series
        Time series.
        
    Returns: 
    ______________________________
    None
        Displays the ACF and PACF graphs for the time series.
    '''
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    plot_acf(timeseries, ax=ax1, lags=75)
    plot_pacf(timeseries, ax=ax2, lags=75)
    plt.show()

def eval(test, pred, plot = True):
    '''
    Evaluates the forecasting performance of a model using Root Mean Squared Error (RMSE), Mean Absolute Error (MAE) and Directional Accuracy metrics.

    Parameters:
    ______________________________
    test: pandas.Series
        Actual time series values. 

    pred: pandas.Series
        Forecasted time series values.

    plot: boolean
        If True, displays a plot of the actual time series values and the predicted time series values. 

    Returns: 
    ______________________________
    None
        Prints the RMSE, MAE and Directional Accuracy evalutation metrics for the input predicted values. 
    '''
    if plot:
        fig, ax = plt.subplots()
        ax.plot(test)
        ax.plot(pred)
        plt.show()
    rmse = mean_squared_error(test, pred, squared=False)
    print(f'Root Mean Squared Error: {rmse}')

    mae = mean_absolute_error(test, pred)
    print(f'Mean Absolute Error: {mae}')
    
    directional_pred = (pred.apply(lambda x: 1 if x > 0 else -1) == test.apply(lambda x: 1 if x > 0 else -1)).sum() / len(test)

    print(f'Directional Accuracy: {directional_pred}')

def transform_series(x, tcode):
    '''
    Transforms a time series based on FRED's recommendations.

    Parameters:
    ______________________________
    x: pandas.Series
        Time series.

    tcode: int.
        Transformation code indicated in FRED's paper: https://fg-research.com/blog/general/posts/fred-md-overview.html

    Returns:
    ______________________________
    pandas.Series
        The transformed time series. 

    Raises:
    ______________________________
    ValueError
        If the input tcode is not one that is used by FRED.
    '''

    if tcode == 1:
        return x
    elif tcode == 2:
        return x.diff()
    elif tcode == 3:
        return x.diff().diff()
    elif tcode == 4:
        return np.log(x)
    elif tcode == 5:
        return np.log(x).diff()
    elif tcode == 6:
        return np.log(x).diff().diff()
    elif tcode == 7:
        return x.pct_change()
    else:
        raise ValueError(f"unknown `tcode` {tcode}")
    
# takes in multiple data frames contating the test data, predictions from the first model and second model
# returns the dmstat, pvalue HAC SE and the mean loss diff
def dm_test(test, pred1, pred2):
    '''
    Conducts the Diebold-Mariano (DM) Test for two time series forecasts. 

    Parameters:
    ______________________________
    test: pandas.Series or pandas.DataFrame
        Contains the actual values of the time series.

    pred1: pandas.Series or pandas.DataFrame
        Contains the values of the time series forecasted by the first model.

    pred2: pandas.Series or pandas.DataFrame
        Contains the values of the time series forecasted by the second model.

    Returns: 
    ______________________________
    dm_stat: float
        The DM statistic of the DM Test.

    p_value: float
        The p-value of the DM Test.

    se: float
        The standard error of the mean of the loss-differential of the two time series forecasts.

    mean: float
        The (realised) mean of the loss-differential of the two time series forecasts.
    '''
    test = np.asarray(test).flatten()
    pred1 = np.asarray(pred1).flatten()
    pred2 = np.asarray(pred2).flatten()
    e1 = pred1-test
    e2= pred2-test
    d = e1**2 - e2**2

    lags = int(50**.33)
    mean = np.mean(d)
    
    resid = d-mean
    model = sm.OLS(resid, np.ones(50))
    model = model.fit(cov_tyoe = 'HAC', cov_kwds={'maxlags':lags, 'kernel':'newey-west'})
    se = model.bse[0]

    dm_stat = mean/se
    p_value = 2 * (1 - scipy.stats.norm.cdf(abs(dm_stat)))

    return dm_stat, p_value, se, mean
