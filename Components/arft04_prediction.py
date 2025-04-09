from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

def arft04_prediction(date = "2020-01-01"):
    train = get_most_recent_series_of_date("GDP", date, fred)
    train = pct_chg(train)

    train = train["pct_chg"]

    start_date_pred = train.index[-1] + pd.offsets.QuarterBegin(1, startingMonth= 1)
    end_date_pred = pd.Period(date, freq='Q').start_time
    
    model = AutoReg(train, lags = 4, trend = 'ct').fit()
    pred = model.predict(start = start_date_pred, end = end_date_pred)

    train = train.to_frame()
    train["Indicator"] = "Actual"
    pred = pred.to_frame().rename(columns = {0: "pct_chg"})
    pred["Indicator"] = "Forecast"

    df = pd.concat([train, pred])
    df.index = pd.to_datetime(df.index).to_period('Q')

    return df

    