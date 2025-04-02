from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

def benchmark1_prediction(date = "2020-01-01"):
    train = get_most_recent_series_of_date("GDP", date, fred)
    train = pct_chg(train)

    train = train["pct_chg"]
    train = train.to_frame()
    train["Indicator"] = "Actual"

    start_date_pred = train.index[-1] + pd.offsets.QuarterBegin(1, startingMonth= 1)
    end_date_pred = pd.Period(date, freq='Q').start_time

    quarter_intervals = pd.date_range(start = start_date_pred, end = end_date_pred, freq = pd.offsets.QuarterBegin(1, startingMonth= 1))

    for quarter in quarter_intervals:
        mean = train["pct_chg"].mean()
        row = pd.DataFrame({"pct_chg": mean, "Indicator": "Forecast"}, index = [quarter])
        train = pd.concat([train, row])

    train.index = pd.to_datetime(train.index).to_period('Q')

    return train
