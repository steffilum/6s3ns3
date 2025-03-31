from fredapi import Fred
import pandas as pd
import os
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc


fred = Fred(api_key='aca56acb87a4241e0e9684e37849de17')

# Example: Pull US CPI data (Seasonally Adjusted)
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

def get_cpi_graph(period=60):
    # get trailing 60 months of data
    cpi_filtered = cpi.iloc[-period:]
    fig = px.line(cpi_filtered, x='MonthYear', y='YOY Change', title='US Consumer Price Index (CPI), Seasonally Adjusted',
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

def get_latest_cpi():
    # Latest Percent Change in CPI round off to 2 dp

    latest_cpi = cpi['YOY Change'].iloc[-1]
    return round(latest_cpi,2)

def get_latest_month():
    latest_month = cpi['MonthYear'].iloc[-1]
    return latest_month

def get_next_release_date():
    latest_date = cpi['Date'].iloc[-1]
    next_date = latest_date + pd.DateOffset(months=2)
    return f"{next_date:%B}, {next_date:%Y}"


##############################################
# Data for core CPI (CPI less food and energy)
##############################################

core_cpi = fred.get_series('CPILFESL')

# convert to DataFrame
core_cpi = core_cpi.reset_index()
core_cpi.columns = ['Date', 'Core CPI']
core_cpi['MonthYear'] = core_cpi['Date'].dt.strftime('%b %Y')

# Calculate year over year change in Core CPI
core_cpi['YOY Change'] = core_cpi['Core CPI'].pct_change(periods=12) * 100

# Calculate monthly over monthly change in Core CPI
core_cpi['MoM Change'] = core_cpi['Core CPI'].pct_change() * 100

# print(core_cpi.tail())

def get_core_cpi_graph(period=60):
    # get trailing 60 months of data
    core_cpi_filtered = core_cpi.iloc[-period:]
    fig = px.line(core_cpi_filtered, x='MonthYear', y='YOY Change', title='US Core Consumer Price Index (CPI) Ex. Food & Energy, Seasonally Adjusted',
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

def get_latest_core_cpi():
    # Latest Percent Change in Core CPI round off to 2 dp

    latest_core_cpi = core_cpi['YOY Change'].iloc[-1]
    return round(latest_core_cpi,2)

def get_latest_core_month():
    latest_core_month = core_cpi['MonthYear'].iloc[-1]
    return latest_core_month

def get_next_core_release_date():
    latest_core_date = core_cpi['Date'].iloc[-1]
    next_core_date = latest_core_date + pd.DateOffset(months=2)
    return f"{next_core_date:%B}, {next_core_date:%Y}"