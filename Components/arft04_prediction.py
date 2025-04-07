from Components.package_imports import *
from Components.data_load import load_data_bridge
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

def arft04_benchmark_prediction_df(date):
    X, y = load_data_bridge(date)
    y.index = pd.to_datetime(y.index).to_period('Q')
    model =  AutoReg(y, lags = 4, trend = 'ct').fit()

    df = y.to_frame().rename(columns = {0: "Actual GDP"})
    predicted_gdp_values =  pd.concat([model.fittedvalues, model.predict(len(y), end = len(y))]).to_frame().rename(columns = {0: "Predicted GDP"})
    df = pd.concat([df, predicted_gdp_values], axis = 1)
    df = df.to_timestamp()
    df.index = df.index.to_period("Q")
    return df
