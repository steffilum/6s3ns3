from package_imports import *

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_pce(given_date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("PCE", given_date, fred)
    pct_chg_pce = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_pce, order=(4, 0, 3), trend = 'c', freq = 'MS').fit(start_params = np.full(4+3+6+1, .01), method_kwargs={'maxiter':200})
    start_date_pred = pct_chg_pce.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_pce, pred])
    print("Consumption data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage
    
# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_biz_equip(date = "2020-01-01", period = 'Q'):
    given_date = "2020-01-01"
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("IPBUSEQ", given_date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_business_equipment = transform_series(df, 5).dropna().diff().dropna()*100
    model = ARIMA(pct_chg_business_equipment, order=(5, 0, 1), trend = 'n', freq = 'MS').fit(start_params = np.full(5+1+1, .01), method_kwargs={'maxiter':200})
    start_date_pred = pct_chg_business_equipment.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_business_equipment, pred])
    print("Business Equipment data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

def quart_pct_chg_business_inventories(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BUSINV", date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_business_inventories = transform_series(df, 5).dropna().diff().dropna()*100
    model = ARIMA(pct_chg_business_inventories, order=(2, 0, 1), trend = 'n', freq = 'MS').fit(start_params = np.full(2+1+1, .01))
    start_date_pred = pct_chg_business_inventories.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_business_inventories, pred])
    print("Business Inventories data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage
    
# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_comm_loans(date = "2020-01-01", period = 'Q'):
    given_date = max("2020-01-01", date)
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BUSLOANS", given_date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_comms_loans = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_comms_loans, order=(2, 0, 12), trend = 'c', freq = 'MS').fit(start_params = np.full(20, .01), method_kwargs={'maxiter':200})
    start_date_pred = pct_chg_comms_loans.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_comms_loans, pred])
    print("Com Loans data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_exports(date = "2020-01-01", period = 'Q'):
    given_date = max("2020-01-01", date)
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BOPTEXP", given_date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_exports = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_exports, order=(5, 0, 5), trend = 'c', freq = 'MS').fit(start_params = np.full(5+5+1+1, .01), method_kwargs={'maxiter':200})
    start_date_pred = pct_chg_exports.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_exports, pred])
    print("Exports data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_govt_constr(date = "2020-01-01", period = 'Q'):
    given_date = max("2020-01-01", date)
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("TLPBLCONS", given_date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_govt_constr = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_govt_constr, order=(1, 0, 1), trend = 'c', freq = 'MS').fit(start_params = np.full(1+1+1+1, .01))
    start_date_pred = pct_chg_govt_constr.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_govt_constr, pred])
    print("Govt Constr data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_defence(date = "2020-01-01"):
    given_date = max("2020-01-01", date)
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("FDEFX", given_date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_fed_defence = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_fed_defence, order=(2, 0, 3), trend = 'c', freq = 'QS').fit(start_params = np.full(2+3+1+1, .01))
    start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.QuarterBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    quarterly_pct_chage = pd.concat([pct_chg_fed_defence, pred])
    print("Defence data Loaded")
    return quarterly_pct_chage

def quart_pct_chg_housing_units_started(given_date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("HOUST", given_date, fred)
    df = df[df.index<pd.Timestamp(given_date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_housing_units_started = transform_series(df, 4).diff().dropna()*100
    model = ARIMA(pct_chg_housing_units_started, order=(1, 0, 1), trend = 'n', freq = 'MS').fit(start_params = np.full(1+1+1, .01))
    start_date_pred = pct_chg_housing_units_started.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_housing_units_started, pred])
    print("Housing data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage
    
def quart_pct_chg_imports(given_date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BOPTIMP", given_date, fred)
    pct_chg_imports = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_imports, order=(3, 0, 4), trend = 'c', freq = 'MS').fit(start_params = np.full(3+4+1+1, .01))
    start_date_pred = pct_chg_imports.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_imports, pred])
    print("Imports data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

def quart_pct_cap(date = "2020-01-01", period = 'Q'):
    given_date = max("2020-01-01", date)
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("ANDENO", given_date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_fed_defence = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_fed_defence, order=(0, 0, 6), trend = 'c', freq = 'MS').fit(start_params = np.full(6+2, .01))
    start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_fed_defence, pred])
    print("Capital Goods data Loaded")
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage

def load_data_bridge(given_date = "2020-01-01"):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("GDP", given_date, fred)
    df = pct_chg(df)
    lag_gdp = df.pct_chg.shift()
    compiled = pd.concat([quart_pct_chg_pce(given_date), quart_pct_chg_govt_constr(given_date),
                      quart_pct_chg_business_inventories(given_date), quart_pct_chg_comm_loans(given_date),
                      quart_pct_chg_exports(given_date), quart_pct_cap(given_date),
                      quart_pct_chg_biz_equip(given_date), quart_pct_chg_defence(given_date),
                      quart_pct_chg_housing_units_started(given_date), quart_pct_chg_imports(given_date),
                      lag_gdp,
                      df.pct_chg], axis = 1).dropna()
    compiled.columns = ['PCE', 'Govt_Constr',
                        'Biz_Inventory', 'Com_Loans',
                        'Exports', 'Capital_Goods',
                        'Biz_Equip', 'Defence',
                        'Housing_Start', 'Import',
                        'Lag_GDP',
                        'GDP']
    X = compiled.iloc[:, :-1]
    y = compiled.GDP   
    print("Bridge Data Loaded") 
    return X, y 

def load_data_rf(given_date = "2020-01-01"):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("GDP", given_date, fred)
    df = pct_chg(df)
    lag_gdp = df.pct_chg.shift()
    compiled = pd.concat([quart_pct_chg_pce(given_date), quart_pct_chg_govt_constr(given_date),
                      quart_pct_chg_business_inventories(given_date), quart_pct_chg_comm_loans(given_date),
                      quart_pct_chg_exports(given_date), quart_pct_cap(given_date),
                      quart_pct_chg_biz_equip(given_date), quart_pct_chg_defence(given_date),
                      quart_pct_chg_housing_units_started(given_date), quart_pct_chg_imports(given_date),
                      lag_gdp,
                      df.pct_chg], axis = 1).dropna()
    compiled.columns = ['PCE', 'Govt_Constr',
                        'Biz_Inventory', 'Com_Loans',
                        'Exports', 'Capital_Goods',
                        'Biz_Equip', 'Defence',
                        'Housing_Start', 'Import',
                        'Lag_GDP',
                        'GDP']
    X = compiled.iloc[:, :-1]
    y = compiled.GDP 
    print("RF data Loaded")   
    return X, y 

def load_data_midas(given_date = "2020-01-01"):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("GDP", given_date, fred)
    df = pct_chg(df)
    lag_gdp = df.pct_chg.shift()
    compiled = pd.concat([quart_pct_chg_pce(given_date, 'M'), quart_pct_chg_govt_constr(given_date, 'M'),
                      quart_pct_chg_business_inventories(given_date, 'M'), quart_pct_chg_comm_loans(given_date, 'M'),
                      quart_pct_chg_exports(given_date, 'M'), quart_pct_cap(given_date, 'M'),
                      quart_pct_chg_biz_equip(given_date, 'M'),
                      quart_pct_chg_housing_units_started(given_date, 'M'), quart_pct_chg_imports(given_date, 'M')], axis = 1).dropna()
    compiled.columns = ['PCE', 'Govt_Constr',
                        'Biz_Inventory', 'Com_Loans',
                        'Exports', 'Capital_Goods',
                        'Biz_Equip',
                        'Housing_Start', 'Import']
    df_q = compiled.groupby(pd.Grouper(freq='Q')).apply(lambda x: x.values.flatten())
    df_q = pd.DataFrame(df_q.tolist(), index=df_q.index)
    df_q.columns = [f"{col}_m{i+1}" for col in compiled.columns for i in range(3)]
    df_q.index = df_q.index.to_period('Q').to_timestamp(how='start')
    compiled = pd.concat([df_q, quart_pct_chg_defence(given_date), lag_gdp, df.pct_chg], axis = 1).dropna()
    compiled.columns.values[-3:] = ['Defence', 'Lag_GDP', 'GDP']
    print("MIDAS data Loaded")  
    return compiled.iloc[:, :-1], compiled.iloc[:, -1]
