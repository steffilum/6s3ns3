import dash
from dash import html, dcc, Input, Output
from shared.default_pagelayout import get_default_layout 
from data.cpi_data import get_cpi_graph, get_latest_cpi, cpi, get_latest_month, get_next_release_date, get_core_cpi_graph, get_latest_core_cpi, get_latest_core_month, get_next_core_release_date

import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/cpi", name="CPI")

cpi_content = html.Div(
    id="main-content",
    style={
       'height': '100vh',
       'overflowY': 'scroll',  # Enable scrolling
       'paddingTop': "50px",   # Leave space on top for nav bar 
       'paddingBottom': '200px' # bottom padding
   },
    children=[
        # Header text container
        html.Div(
            children=[
                html.H1(
                    "Consumer Price Index (CPI)",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "32px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                )
            ],
            style={"textAlign": "center"}
        ),
        html.Br(),
        # Container for the graph and the button overlay
        html.Div(
            style={
                "position": "relative",
                "maxWidth": "1000px",
                "margin": "0 auto"
            },
            children=[
                # Graph
                dcc.Graph(
                    id="cpi-graph",
                    figure=get_cpi_graph(60),
                    style={"height": "400px", "width": "100%"},
                    config={"displayModeBar": False}
                ),
                html.Div(
                    children = [
                dbc.Button(
                    "1y",
                    id="1y-button",
                    size="sm",
                     style={
                        "position": "absolute",
                        "top": "10px",       
                        "right": "102px",     
                        "zIndex": "1000",    # Ensures it sits on top
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                ), 
                dbc.Button(
                    "5y",
                    id="5y-button",
                    size="sm",
                    style={
                        "position": "absolute",
                        "top": "10px",
                        "right": "150px",
                        "zIndex": "1000",
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                ),
                dbc.Button(
                    "10y", 
                    id="10y-button",
                    size= 'sm',
                    style ={ 
                        "position": "absolute",
                        "top": "10px",       
                        "right": "197px",     
                        "zIndex": "1000",    
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                ), 
                dbc.Button(
                    'All', 
                    id= 'all-button',
                    size = 'sm',
                    style = {
                        "position": "absolute",
                        "top": "10px",
                        "right": "250px",
                        "zIndex": "1000",
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                )
                    ], 
                    style = {
                        "position": "absolute",
                        "top": "10px",
                        "right": "-100px",  # Adjust as needed to move them further/closer to the right edge
                        "zIndex": "1000",
                        "display": "flex",      # Optional: to lay them out in a row
                        "gap": "20px" }
                )
                
                
            ]
        ),
        # Latest CPI value
        html.Div(
            children=[
                html.H3(
                    f"Latest CPI Number as of {get_latest_month()}: {get_latest_cpi()}%",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ), 
                html.H4(
                    f"Next release of CPI data is scheduled for at {get_next_release_date()}.",
                    style={
                        "color": "grey", 
                        "fontSize": "14px",
                        "fontFamily": "Montserrat, sans-serif",
                        "fontWeight": "400",
                        "fontStyle": "italic", 
                        "marginLeft": "0px"
                    }
                )
            ],
            style={
                "marginTop": "30px",
                "marginLeft": "170px"
            }
        ), 
        html.Br(), 
        html.Br(),
        # Core CPI Graph
        html.Div(
            style={
                "position": "relative",
                "maxWidth": "1000px",
                "margin": "0 auto"
            },
            children=[
                # Header text container
                html.Div(
                    children=[
                        html.H1(
                            "Core Consumer Price Index (Core-CPI)",
                            style={
                                "color": "white",
                                "fontWeight": "600",
                                "fontSize": "32px",
                                "fontFamily": "Montserrat, sans-serif"
                            }
                        )
                    ],
                    style={"textAlign": "center"}
                ),
                # Graph
                html.Br(),
                dcc.Graph(
                    id="core-cpi-graph",
                    figure=get_core_cpi_graph(60),
                    style={"height": "400px", "width": "100%"},
                    config={"displayModeBar": False}
                ),
                html.Div(
                    children = [
                dbc.Button(
                    "1y",
                    id="core-1y-button",
                    size="sm",
                     style={
                        "position": "absolute",
                        "top": "10px",       
                        "right": "102px",     
                        "zIndex": "1000",    # Ensures it sits on top
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                ), 
                dbc.Button(
                    "5y",
                    id="core-5y-button",
                    size="sm",
                    style={
                        "position": "absolute",
                        "top": "10px",
                        "right": "150px",
                        "zIndex": "1000",
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                ),
                dbc.Button(
                    "10y", 
                    id="core-10y-button",
                    size= 'sm',
                    style ={ 
                        "position": "absolute",
                        "top": "10px",       
                        "right": "197px",     
                        "zIndex": "1000",    
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                ), 
                dbc.Button(
                    'All', 
                    id= 'core-all-button',
                    size = 'sm',
                    style = {
                        "position": "absolute",
                        "top": "10px",
                        "right": "250px",
                        "zIndex": "1000",
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                )
                    ], 
                    style = {
                        "position": "absolute",
                        "top": "70px",
                        "right": "-100px",  # Adjust as needed to move them further/closer to the right edge
                        "zIndex": "1000",
                        "display": "flex",      # Optional: to lay them out in a row
                        "gap": "20px" }
                )
                
                
            ]
        ),
        # Latest Core CPI value
        html.Div(
            children=[
                html.H3(
                    f"Latest Core-CPI Number as of {get_latest_core_month()}: {get_latest_core_cpi()}%",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ), 
                html.H4(
                    f"Next release of CPI data is scheduled for at {get_next_core_release_date()}.",
                    style={
                        "color": "grey", 
                        "fontSize": "14px",
                        "fontFamily": "Montserrat, sans-serif",
                        "fontWeight": "400",
                        "fontStyle": "italic", 
                        "marginLeft": "0px"
                    }
                )
            ],
            style={
                "marginTop": "30px",
                "marginLeft": "170px"
            }
        ), 
        html.Br(),
        html.Br(),
        html.Div(
            children=[
                html.H3(
                    "What is the Consumer Price Index (CPI)?",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "32px",
                        "fontFamily": "Montserrat, sans-serif", 
                        "textalign": "center"
                    }
                )
            ], style={"textAlign": "center"}
        ), 
        html.Div(
            children = [
                html.P("The Consumer Price Index (CPI) is a measure of the average change over time in the prices paid by urban consumers for a market basket of consumer goods and services. Core CPI is an aggregate of prices paid by urban consumers for a typical basket of goods, excluding food and energy. This measurement is widely used by economists because food and energy have very volatile prices. The CPI is a key economic indicator used to measure inflation and changes in purchasing trends. The CPI is published monthly by the Bureau of Labor Statistics (BLS). This data is taken from FRED."
                )
            ], style = {
                "marginLeft": "100px",
                "marginRight": "100px",
                "marginTop": "20px",
                "color": "white",
                "fontSize": "18px",
                "fontFamily": "Montserrat, sans-serif"
            }
                              

        )
    ]
)

layout = get_default_layout(main_content=cpi_content)



@dash.callback(
    Output("cpi-graph", "figure"),
    Input("1y-button", "n_clicks"), 
    Input("5y-button", "n_clicks"),
    Input("10y-button", "n_clicks"), 
    Input("all-button", "n_clicks")
)
def update_cpi_graph(n_clicks_1, n_clicks_5, n_clicks_10, n_clicks_all):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Use the button id to decide which period to display
    if button_id == "10y-button":
        fig = get_cpi_graph(120)  # 10-year data
    elif button_id == "1y-button":
        fig = get_cpi_graph(12)  # 1-year data
    elif button_id == "5y-button":
        fig = get_cpi_graph(60) # 5-year data
    elif button_id == "all-button":
        fig = get_cpi_graph(len(cpi))
    else:
        # Fallback to a default state
        fig = get_cpi_graph(60)
    
    # Force the figure to a fixed size
    fig.update_layout(autosize=False, width=1000, height=400)
    return fig


@dash.callback(
    Output("core-cpi-graph", "figure"),
    Input("core-1y-button", "n_clicks"), 
    Input("core-5y-button", "n_clicks"),
    Input("core-10y-button", "n_clicks"), 
    Input("core-all-button", "n_clicks")
)
def update_core_cpi_graph(n_clicks_1, n_clicks_5, n_clicks_10, n_clicks_all):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Use the button id to decide which period to display
    if button_id == "core-10y-button":
        fig = get_core_cpi_graph(120)  # 10-year data
    elif button_id == "core-1y-button":
        fig = get_core_cpi_graph(12)  # 1-year data
    elif button_id == "core-5y-button":
        fig = get_core_cpi_graph(60) # 5-year data
    elif button_id == "core-all-button":
        fig = get_core_cpi_graph(len(cpi))
    else:
        # Fallback to a default state
        fig = get_core_cpi_graph(60)
    
    # Force the figure to a fixed size
    fig.update_layout(autosize=False, width=1000, height=400)
    return fig
