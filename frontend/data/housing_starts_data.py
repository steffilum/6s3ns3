from fredapi import Fred
import pandas as pd
import os
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc


fred = Fred(api_key='aca56acb87a4241e0e9684e37849de17')

##############################################
# Data for Housing Starts
##############################################

housing_starts = fred.get_series('HOUST')

# convert to DataFrame
housing_starts = housing_starts.reset_index()
housing_starts.columns = ['Date', 'housingstarts']
housing_starts['MonthYear'] = housing_starts['Date'].dt.strftime('%b %Y')

# Start data from 1993
housing_starts = housing_starts[housing_starts['Date'] >= pd.Timestamp('1993-01-01')]

# Calculate year over year change in Housing Starts
housing_starts['YOY Change'] = housing_starts['housingstarts'].pct_change(periods=12) * 100

# Calculate monthly over monthly change in Housing Starts
housing_starts['MoM Change'] = housing_starts['housingstarts'].pct_change() * 100

# For plotting yoy and mom change in housing starts
# def get_housingstarts_graph(period=60):
#     # get trailing period of data
#     housingstarts = housing_starts.iloc[-period:].copy()
    
#     # Reshape for multiple lines
#     df_melted = housingstarts.melt(
#         id_vars=['MonthYear'],
#         value_vars=['YOY Change', 'MoM Change'],
#         var_name='Change Type',
#         value_name='Change (%)'
#     )
    
#     fig = px.line(
#         df_melted,
#         x='MonthYear',
#         y='Change (%)',
#         color='Change Type',
#         title='New Privately-Owned Housing Units Started (YoY vs MoM)',
#         labels={"MonthYear": "", "Change Type": "", "Change (%)": "Change (%)"},
#         template='plotly_dark'
#     )
    
#     # Styling
#     fig.update_xaxes(showgrid=False)
#     fig.update_yaxes(showgrid=False)
    
#     fig.update_layout(
#         autosize=True,
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(l=0, r=0, t=50, b=50),
#         title={
#             "font": {
#                 "color": "grey",
#                 "family": "Montserrat, sans-serif"
#             }
#         },
#         height=250  # Adjust as needed
#     )
#     return fig

def get_housingstarts_graph(period=60):
    # get trailing 60 months of data
    housingstarts = housing_starts.iloc[-period:]
    fig = px.line(housingstarts, x='MonthYear', y='YOY Change', title='New Privately-Owned Housing Units Started',
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



def get_latest_housingstarts():
    # Latest Percent Change in CPI round off to 2 dp

    latest_housingstart = housing_starts['YOY Change'].iloc[-1]
    return round(latest_housingstart,2)

def get_latest_month():
    latest_month = housing_starts['MonthYear'].iloc[-1]
    return latest_month

def get_next_release_date():
    latest_date = housing_starts['Date'].iloc[-1]
    next_date = latest_date + pd.DateOffset(months=2)
    return f"{next_date:%B}, {next_date:%Y}"