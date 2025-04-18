import dash
from dash import html, dcc, Input, Output
from shared.default_pagelayout import get_default_layout 
from data.housing_starts_data import housing_starts, get_housingstarts_graph, get_latest_housingstarts, get_latest_month, get_next_release_date
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/housing_starts", name="Housing Starts")

housingstarts_content = html.Div(
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
                    "Housing Starts in the US",
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
                    id="housingstarts-graph",
                    figure=get_housingstarts_graph(60),
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
                        "zIndex": "1000",    
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
                        "right": "-100px",  
                        "zIndex": "1000",
                        "display": "flex",      
                        "gap": "20px" }
                )
                
                
            ]
        ),
        # Latest Housing Starts value
        html.Div(
            children=[
                html.H3(
                    f"Latest Year over Year percentage change in Housing Starts as of {get_latest_month()}: {get_latest_housingstarts()}%",
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
                    "What is Housing Starts?",
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
                html.P("Housing Starts is an economic indicator that measures the number of new residential construction projects that have begun during any particular month. The U.S. Census Bureau and the U.S. Department of Housing and Urban Development jointly release the data on a monthly basis. The data is used to gauge the health of the housing market and the overall economy. A high number of housing starts is generally seen as a positive sign for the economy, as it indicates that builders are confident in the market and are investing in new construction projects. Conversely, a low number of housing starts can be a sign of a weak economy, as it suggests that builders are hesitant to invest in new projects."
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

layout = get_default_layout(main_content=housingstarts_content)

@dash.callback(
    Output("housingstarts-graph", "figure"),
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
        fig = get_housingstarts_graph(120)  # 10-year data
    elif button_id == "1y-button":
        fig = get_housingstarts_graph(12)  # 1-year data
    elif button_id == "5y-button":
        fig = get_housingstarts_graph(60) # 5-year data
    elif button_id == "all-button":
        fig = get_housingstarts_graph(len(housing_starts))
    else:
        # Fallback to a default state
        fig = get_housingstarts_graph(60)
    
    # Force the figure to a fixed size
    fig.update_layout(autosize=False, width=1000, height=400)
    return fig
