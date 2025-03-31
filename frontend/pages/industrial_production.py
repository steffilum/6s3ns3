import dash
from dash import html, dcc, Input, Output
from shared.default_pagelayout import get_default_layout 
from data.indust_p_data import indust_p, get_iprodcution_graph, get_latest_iproduction, get_latest_month, get_next_release_date
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/industrial_production", name="Industrial Production")

iproduction_content = html.Div(
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
                    "Industrial Production in the US",
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
                    id="iproduction-graph",
                    figure=get_iprodcution_graph(60),
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
        # Latest Housing Starts value
        html.Div(
            children=[
                html.H3(
                    f"Latest Year over Year percentage change in Industrial Production as of {get_latest_month()}: {get_latest_iproduction()}%",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ), 
                html.H4(
                    f"Next release of Housing Starts data is scheduled for at {get_next_release_date()}.",
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
                    "What is Industrial Production?",
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
                html.P("Industrial production is the measure of the output of the industrial sector of the economy. It includes mining, manufacturing, and utilities. This data is released monthly by the Federal Reserve and is a key indicator of the health of the economy. A rising industrial production number indicates a growing economy, while a falling number indicates a shrinking economy. The industrial production index is a measure of the physical output of the nation's factories, mines, and utilities. The index is compiled by the Federal Reserve and is based on data from the Industrial Production and Capacity Utilization statistical program. The index is calculated using a weighted formula that includes the output of the manufacturing, mining, and utilities sectors. The index is reported as a percentage change from the previous month and is seasonally adjusted to account for variations in production due to factors such as weather, holidays, and other seasonal factors."
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

layout = get_default_layout(main_content=iproduction_content)

@dash.callback(
    Output("iproduction-graph", "figure"),
    Input("1y-button", "n_clicks"), 
    Input("5y-button", "n_clicks"),
    Input("10y-button", "n_clicks"), 
    Input("all-button", "n_clicks")
)
def update_iproduction_graph(n_clicks_1, n_clicks_5, n_clicks_10, n_clicks_all):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Use the button id to decide which period to display
    if button_id == "10y-button":
        fig = get_iprodcution_graph(120)  # 10-year data
    elif button_id == "1y-button":
        fig = get_iprodcution_graph(12)  # 1-year data
    elif button_id == "5y-button":
        fig = get_iprodcution_graph(60) # 5-year data
    elif button_id == "all-button":
        fig = get_iprodcution_graph(len(indust_p))
    else:
        # Fallback to a default state
        fig = get_iprodcution_graph(60)
    
    # Force the figure to a fixed size
    fig.update_layout(autosize=False, width=1000, height=400)
    return fig
