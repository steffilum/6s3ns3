import pandas as pd
import numpy as np
import plotly.express as px

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
#print(gdp_growth_df["Quarter"].max())



# Define function to get GDP growth rate for quarter
def get_gdp_growth_rate(quarter):
    return gdp_growth_df.loc[gdp_growth_df["Quarter"] == quarter, "GDP_Growth_Rate"].values[0] 

# Define function to plot GDP growth rate range
def get_forecast_graph(start_quarter, end_quarter): 
    
    # Get GDP growth rate from start until selected quarter
    df_filtered = gdp_growth_df.loc[
        (gdp_growth_df["Date"] >= start_quarter) & (gdp_growth_df["Date"] <= end_quarter)
    ]
    
    # Create a line plot
    fig = px.line(
        df_filtered,
        x = 'Date',
        y='GDP_Growth_Rate',
        title=f"GDP Growth Rate from {start_quarter} to {end_quarter}",
        labels={"GDP_Growth_Rate": "GDP Growth Rate (%)"},
        template='plotly_dark'
    )
    
    # Extract the date corresponding to the selected quarter for the vertical line
    start_date = pd.to_datetime(
        gdp_growth_df.loc[gdp_growth_df["Quarter"] == start_quarter, "Date"].iloc[0]
    )
    end_date = pd.to_datetime(
        gdp_growth_df.loc[gdp_growth_df["Quarter"] == end_quarter, "Date"].iloc[0]
    )
    
    # Add a vertical line at the selected quarters
    fig.add_vline(x=end_date, line_dash="dash", line_color="red")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plotting area
        margin=dict(l=0, r=0, t=50, b=50)
    )

    
    return fig 

