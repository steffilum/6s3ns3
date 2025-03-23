import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os

# Set working directory to current file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))


dash.register_page(__name__, path="/", name="Home") # Register the homepage

# Homepage layout
layout = html.Div(
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
        html.Nav(
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

                    html.Button("Indicators", id="fade-button", n_clicks=0, style={
                        "position": "absolute",
                        "left": "856px",
                        "top": "42px",
                        "backgroundColor": "transparent",
                        "border": "none",
                        "color": "rgba(206, 203, 203, 0.8)",
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "22px",
                        "cursor": "pointer"
                    })
                ])
            ]
        ),

        # Fade Dropdown
        dbc.Fade(
            id="fade",
            is_in=False,
            appear=True,
            children=html.Div(
                className="mega-dropdown",
                children=[
                    html.Div("Explore Indicators", className="dropdown-item-normal"),
                    dcc.Link("CPI", href="/cpi", className="dropdown-item-bold"),
                    html.Div("Housing Starts", className="dropdown-item-bold"),
                    html.Div("PMI", className="dropdown-item-bold")
                ]
            )
        ),

        # Main content (blurs when dropdown is open)
        html.Div(
            id="main-content",
            className="main-content",
            style={"position": "absolute", "top": "150px", "left": "150px", "width": "300px"},
            children=[
                html.P("This is a placeholder for the main content of the page", style={"textAlign": "center"}),
            ]
        )
    ]
)

# Callback to toggle dropdown visibility and blur content
@dash.callback(
    Output("fade", "is_in"),
    Output("main-content", "className"),
    Input("fade-button", "n_clicks"),
    State("fade", "is_in")
)
def toggle_fade(n, is_in):
    if not n:
        return False, "main-content"
    show = not is_in
    return show, "main-content blur-content" if show else "main-content"


if __name__ == "__main__":
    app.run(debug=True)
