from fredapi import Fred
import pandas as pd

my_key = 'aca56acb87a4241e0e9684e37849de17'
fred = Fred(api_key=my_key)

cpi_data = fred.get_series('CPIAUCSL')

# calculate yoy inflation
cpi_yoy = cpi_data.pct_change(periods=12) * 100

df = cpi_data.reset_index()
df.columns = ['date', 'cpi']
print(df.tail())

