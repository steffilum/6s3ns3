import pandas as pd
import numpy as np

# Generate date range from 1950Q1 to 2023Q4
dates = pd.date_range(start="1950-01-01", end="2023-12-31", freq='Q')

n_periods = len(dates)

# Set random seed for reproducibility
np.random.seed(42)

# Simulate GDP growth rate with a realistic mean and volatility
# Let's assume mean ~0.8% per quarter (3.2% annualized), std ~1%
gdp_growth = np.random.normal(loc=0.8, scale=1.0, size=n_periods)

# Create DataFrame
gdp_growth_df = pd.DataFrame({
    "Date": dates,
    "GDP_Growth_Rate": gdp_growth
})



#create a column for year and quarter
gdp_growth_df['Quarter'] = (
    pd.PeriodIndex(pd.to_datetime(gdp_growth_df['Date']), freq='Q')
    .astype(str)
)

# Optional: Display first few rows
#print(gdp_growth_df.head())




# Define function to get GDP growth rate for quarter
def get_gdp_growth_rate(quarter):
    return gdp_growth_df.loc[gdp_growth_df["Quarter"] == quarter, "GDP_Growth_Rate"].values[0]
    