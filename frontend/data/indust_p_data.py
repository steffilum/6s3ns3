from fredapi import Fred
import pandas as pd
import os
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc


fred = Fred(api_key='aca56acb87a4241e0e9684e37849de17')

##############################################
# Data for Industrial Production
##############################################

indust_p = fred.get_series('IPBUSEQ')

# convert to DataFrame
indust_p = indust_p.reset_index()
indust_p.columns = ['Date', 'industrialproduction']
indust_p['MonthYear'] = indust_p['Date'].dt.strftime('%b %Y')

# Start data from 1993
indust_p = indust_p[indust_p['Date'] >= pd.Timestamp('1993-01-01')]

# Calculate year over year change in Housing Starts
indust_p['YOY Change'] = indust_p['industrialproduction'].pct_change(periods=12) * 100

# Calculate monthly over monthly change in Housing Starts
indust_p['MoM Change'] = indust_p['industrialproduction'].pct_change() * 100

# print(indust_p.tail())

def get_iprodcution_graph(period=60):
    # get trailing 60 months of data
    iproduction = indust_p.iloc[-period:]
    fig = px.line(iproduction, x='MonthYear', y='YOY Change', title='Industrial Production Index',
                  labels={"MonthYear": "", "YOY Change": "YOY Change (%)"}, template='plotly_dark')
    
    # Remove grid lines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plotting area
        margin=dict(l=0, r=0, t=50, b=50),
        title={
            "font": {
                "color": "grey",
                "family": "Montserrat, sans-serif"
            }
        },
        height=200
    )
    return fig

def get_latest_iproduction():
    # Latest Percent Change in iproduction round off to 2 dp
    latest_iproduction = indust_p['YOY Change'].iloc[-1]
    return round(latest_iproduction,2)

def get_latest_month():
    latest_month = indust_p['MonthYear'].iloc[-1]
    return latest_month

def get_next_release_date():
    latest_date = indust_p['Date'].iloc[-1]
    next_date = latest_date + pd.DateOffset(months=2)
    return f"{next_date:%B}, {next_date:%Y}"

