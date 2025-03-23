import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from animation import get_fade_component
import os

# Set working directory to current file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


# App layout
app.layout = html.Div(
    style={
        "height": "100vh",
        "background": "radial-gradient(circle at top left, #3e1f47 0%, #000000 25%)",
        "boxShadow": "0 0 100px #ff6a00",
        "margin": "0px",
        "padding": "0px",
        "position": "relative",
        "overflow": "hidden"
    },
    children=[
        html.Nav(                                           # Navigation bar
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "padding": "20px 40px",
                "color": "rgba(206, 203, 203, 0.8)",
                "fontFamily": "Montserrat, sans-serif",
                "fontWeight": "400",
                "fontSize": "22px"
            },
            children=[
                # Logo
                html.Div("6SENS3", style={                     
                    "fontWeight": "800",
                    "color": "white",
                    "fontSize": "32px", 
                    "position": "absolute",
                    "left": "75px",
                    "top": "35px"
                }),

                # Navigation items + dropdown
                html.Div([
                    html.Span("About", style={
                        "cursor": "default", 
                        "position": "absolute", 
                        "left": "482px", 
                        "top": "42px"
                    }),

                    html.Span("Models", style={
                        "cursor": "default", 
                        "position": "absolute", 
                        "left": "669px", 
                        "top": "42px"
                    }),

                    # Dropdown menu
                    dbc.DropdownMenu(
                        label="Indicators",
                        nav=True,
                        in_navbar=True,
                        direction="down",
                        className="mega-dropdown", 
                        style={
                            "position": "absolute",
                            "left": "856px",
                            "top": "42px",
                            "backgroundColor": "transparent",
                            "border": "none"
                        },
                        children=[
                            dbc.DropdownMenuItem("Explore Indicators", className="dropdown-item-normal"),
                            dbc.DropdownMenuItem("CPI", className="dropdown-item-bold"),
                            dbc.DropdownMenuItem("Housing Starts", className="dropdown-item-bold"),
                            dbc.DropdownMenuItem("PMI", className="dropdown-item-bold")
                        ]
                    )
                ])
            ]
        ), 
        html.Div(id="fade-section-container")
    ]
)


# Fade callback
@app.callback(
    Output("fade", "is_in"),
    Input("fade-button", "n_clicks"),
    State("fade", "is_in")
)
def toggle_fade(n, is_in):
    if not n:
        return False
    return not is_in



if __name__ == "__main__":
    app.run(debug=True)
