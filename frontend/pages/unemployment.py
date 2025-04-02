import dash
from dash import html, dcc, Input, Output
from shared.default_pagelayout import get_default_layout 
from data.unemployment_data import unemployment, get_unemployment_graph, get_latest_unemployment_change, get_latest_month, get_next_release_date, get_next_month, openings, get_openings_graph, get_latest_month_openings, get_latest_openings_change, get_next_month_openings,get_next_release_date_openings, get_latest_openingsfigure
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/unemployment", name="Unemployment Rate")

uemployment_content = html.Div(
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
                    "Unemployment Rate in the US",
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
                    id="uemployment-graph",
                    figure=get_unemployment_graph(60),
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
        # Latest Unemployment value
        html.Div(
            children=[
                html.H3(
                    f"Latest MoM % change in Unemployment Rate as of {get_latest_month()}: {get_latest_unemployment_change()}%",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ), 
                html.H4(f"Latest Unemployment Rate as of {get_latest_month()}: {unemployment['unemployment'].iloc[-1]}%",
                 style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ), 
                html.H5(
                    f"Next release of Unemployment data for {get_next_month()} is scheduled for at {get_next_release_date()}.",
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
                    "What is Unemployment Rate?",
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
                html.P("""
                The unemployment rate represents the number of unemployed as a percentage of the labor force. Labor force data are restricted to people 16 years of age and older, who currently reside in 1 of the 50 states or the District of Columbia, who do not reside in institutions (e.g., penal and mental facilities, homes for the aged), and who are not on active duty in the Armed Forces.
                This rate is also defined as the U-3 measure of labor underutilization. It is a key economic indicator used to gauge the health of an economy.
                """
                )
            ], style = {
                "marginLeft": "100px",
                "marginRight": "100px",
                "marginTop": "20px",
                "color": "lightgrey",
                "fontSize": "18px",
                "fontFamily": "Montserrat, sans-serif"
            }
                              

        ),
        html.Br(),
        html.Br(),
        html.Br(),
        # Container for the graph and the button overlay
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
                            "Total Nonfarm Job Openings in the US",
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
                    id="openings-graph",
                    figure=get_openings_graph(60),
                    style={"height": "400px", "width": "100%"},
                    config={"displayModeBar": False}
                ),
                html.Div(
                    children = [
                dbc.Button(
                    "1y",
                    id="openings-1y-button",
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
                    id="openings-5y-button",
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
                    id="openings-10y-button",
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
                    id= 'openings-all-button',
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
        html.Div(
            children=[
                html.H3(
                    f"Latest MoM % change in Nonfarm Job Openings Rate as of {get_latest_month_openings()}: {get_latest_openings_change()}%",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ), 
                html.H4(f"Latest Total Number of Nonfarm Job Openings as of {get_latest_month_openings()}: {get_latest_openingsfigure()}",
                 style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ), 
                html.H5(
                    f"Next release of Total Nonfarm Job Openings data for {get_next_month_openings()} is scheduled for at {get_next_release_date_openings()}.",
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
                    "What are Total Nonfarm Job Openings?",
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
                html.P("""
                The Job Openings and Labor Turnover Survey (JOLTS) program produces data on job openings, hires, and separations. 
                Total Nonfarm Job Openings are a measure of all jobs that are not filled on the last business day of the month. A job is considered open if a specific position exists and there is work available for it, the job can be started within 30 days, and there is active recruiting for the position.
                These data help to provide insight into the labor market. Job openings are a measure of demand for labor. 
                Job openings are a component of the Job Openings and Labor Turnover Survey (JOLTS) program. 
                Job openings are a measure of labor demand. Job openings are a count of the number of job openings on the last business day of the month.
                """
                )
            ], style = {
                "marginLeft": "100px",
                "marginRight": "100px",
                "marginTop": "20px",
                "color": "lightgrey",
                "fontSize": "18px",
                "fontFamily": "Montserrat, sans-serif"
            }
                              

        )
    ]
)

layout = get_default_layout(main_content=uemployment_content)

@dash.callback(
    Output("uemployment-graph", "figure"),
    Input("1y-button", "n_clicks"), 
    Input("5y-button", "n_clicks"),
    Input("10y-button", "n_clicks"), 
    Input("all-button", "n_clicks")
)
def update_housingstarts_graph(n_clicks_1, n_clicks_5, n_clicks_10, n_clicks_all):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Use the button id to decide which period to display
    if button_id == "10y-button":
        fig = get_unemployment_graph(120)  # 10-year data
    elif button_id == "1y-button":
        fig = get_unemployment_graph(12)  # 1-year data
    elif button_id == "5y-button":
        fig = get_unemployment_graph(60) # 5-year data
    elif button_id == "all-button":
        fig = get_unemployment_graph(len(unemployment))
    else:
        # Fallback to a default state
        fig = get_unemployment_graph(60)
    
    # Force the figure to a fixed size
    fig.update_layout(autosize=False, width=1000, height=400)
    return fig

@dash.callback(
    Output("openings-graph", "figure"),
    Input("openings-1y-button", "n_clicks"), 
    Input("openings-5y-button", "n_clicks"),
    Input("openings-10y-button", "n_clicks"), 
    Input("openings-all-button", "n_clicks")
)
def update_core_cpi_graph(n_clicks_1, n_clicks_5, n_clicks_10, n_clicks_all):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Use the button id to decide which period to display
    if button_id == "openings-10y-button":
        fig = get_openings_graph(120)  # 10-year data
    elif button_id == "openings-1y-button":
        fig = get_openings_graph(12)  # 1-year data
    elif button_id == "openings-5y-button":
        fig = get_openings_graph(60) # 5-year data
    elif button_id == "openings-all-button":
        fig = get_openings_graph(len(openings))
    else:
        # Fallback to a default state
        fig = get_openings_graph(60)
    
    # Force the figure to a fixed size
    fig.update_layout(autosize=False, width=1000, height=400)
    return fig

