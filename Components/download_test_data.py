from package_imports import *
from data_load import *

given_date = "2020-03-01"

for index in range(1, 81):
    date = pd.to_datetime(given_date)
    new_date = date - pd.DateOffset(months=3*index)
    new_date_str = new_date.strftime('%Y-%m-%d')
    X_train, y_train = load_data_bridge(new_date_str)
    with open(f'Components/test_data_bridge/data_iteration_{new_date_str}.pkl', 'wb') as f:
        pickle.dump((X_train, y_train), f)

# for index in range(51, 81):
#     date = pd.to_datetime(given_date)
#     new_date = date - pd.DateOffset(months=3*index)
#     new_date_str = new_date.strftime('%Y-%m-%d')
#     X_train, y_train = load_data_midas(new_date_str)
#     with open(f'Components/test_data_midas/data_iteration_{new_date_str}.pkl', 'wb') as f:
#         pickle.dump((X_train, y_train), f)


# with open('Components/test_data_midas/data_iteration_2007-09-01.pkl', 'rb') as f:
#     df, series = pickle.load(f)
# print(df, series)

# with open('Components/test_data_bridge/data_iteration_1999-12-01.pkl', 'rb') as f:
#     df, series = pickle.load(f)
# print(series)
