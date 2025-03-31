import dash
from dash import html, dcc, Input, Output
from shared.default_pagelayout import get_default_layout 
from data.cpi_data import get_cpi_graph, get_latest_cpi, cpi, get_latest_month, get_next_release_date
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/cpi", name="CPI")

cpi_content = html.Div(
    id="main-content",
    style={
       'height': '100vh',
       'overflowY': 'scroll',  # Enable scrolling
       'paddingTop': "50px",   # Leave space on top for nav bar 
       'paddingBottom': '100px' # bottom padding
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
