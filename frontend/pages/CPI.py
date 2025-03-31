import dash
from dash import html, dcc, Input, Output
from shared.default_pagelayout import get_default_layout 
from data.cpi_data import get_cpi_graph, get_latest_cpi
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
                # Button positioned on top of the graph
                dbc.Button(
                    "1y",
                    id="1y-button",
                    size="sm",
                    style={
                        "position": "absolute",
                        "top": "10px",       
                        "right": "150px",     
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
                    size= 'sm',
                    style ={ 
                        "position": "absolute",
                        "top": "10px",       
                        "right": "100px",     
                        "zIndex": "1000",    
                        "backgroundColor": "grey",
                        "color": "white",
                        "border": "none",
                        "padding": "4px 8px",
                        "fontSize": "14px"
                    }
                )
            ]
        ),
        # Latest CPI value
        html.Div(
            children=[
                html.H3(
                    f"Latest CPI Number: {get_latest_cpi()}%",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                )
            ],
            style={
                "marginTop": "30px",
                "marginLeft": "150px"
            }
        ), 
        dcc.Graph(
            id = '',
            figure=get_cpi_graph(60)
           
        )
    ]
)

layout = get_default_layout(main_content=cpi_content)

@dash.callback(
    Output("cpi-graph", "figure"),
    Input("1y-button", "n_clicks")
)
def update_cpi_graph(n_clicks):  
    # Determine which period to use based on button clicks
    if not n_clicks or n_clicks % 2 == 0:
        fig = get_cpi_graph(60)
    else:
        fig = get_cpi_graph(12)
    
    # Force the figure to a fixed size
    fig.update_layout(autosize=False, width=1000, height=400)
    return fig
