from fredapi import Fred
import pandas as pd
import os
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc


fred = Fred(api_key='aca56acb87a4241e0e9684e37849de17')

# Example: Pull US CPI data (Not Seasonally Adjusted)
cpi = fred.get_series('CPIAUCNS')

# convert to DataFrame
cpi = cpi.reset_index()
cpi.columns = ['Date', 'CPI']
cpi['MonthYear'] = cpi['Date'].dt.strftime('%b %Y')

# Calculate year over year change in CPI
cpi['YOY Change'] = cpi['CPI'].pct_change(periods=12) * 100

# Calculate monthly over monthly change in CPI
cpi['MoM Change'] = cpi['CPI'].pct_change() * 100


#print(cpi.tail())

def get_cpi_graph():
    # get trailing 60 months of data
    cpi_filtered = cpi.iloc[-60:]
    fig = px.line(cpi_filtered, x='MonthYear', y='YOY Change', title='US Consumer Price Index (CPI)',
                  labels={"MonthYear": "Month"}, template='plotly_dark')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plotting area
        margin=dict(l=0, r=0, t=50, b=50),
        title={
            "text": "Monthly % Change in CPI (MoM)",
            "font": {
                "color": "grey",
                "family": "Montserrat, sans-serif"
            }
        },
        height=200
    )
    return fig

def get_latest_cpi():
    latest_cpi = cpi['CPI'].iloc[-1]
    return latest_cpi



cpi_card = {
    "key": "cpi-slide",
    "children": html.Div(
        style={
            "width": "100%"
        },
        children=[
            html.H2(f"CPI: {get_latest_cpi():+.1f}%"),
            dcc.Graph(
                figure=get_cpi_graph(),
                config={"displayModeBar": False}
            )
        ]
    )
}
