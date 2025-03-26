import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Main layout definition
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
        # Navigation Bar
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
                # Logo that clicks to return to homepage
                dcc.Link("6SENS3", href='/', style={                     
                    "fontWeight": "800",
                    "fontSize": "32px", 
                    "position": "absolute",
                    "left": "75px",
                    "top": "35px",
                    "textDecoration": "none"},
                    className="logo-clickable"
                ),

                html.Div([
                    # About button as a link
                    dcc.Link("About", href="/about", style={
                        "position": "absolute",
                        "left": "482px",
                        "top": "42px",
                        "backgroundColor": "transparent",
                        "border": "none",
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "22px",
                        "cursor": "pointer",
                        "textDecoration": "none" 
                    }, className="fade-button-dropdown"),

                    html.Button("Models", id="model-fade-button", className= 'fade-button-dropdown', n_clicks=0, style={
                        "cursor": "pointer", 
                        "position": "absolute", 
                        "left": "669px", 
                        "top": "42px",
                        "backgroundColor": "transparent",
                        "border": "none",
                        
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "22px"
                    }),

                    html.Button("Indicators", id="indicator-fade-button", className= 'fade-button-dropdown', n_clicks=0, style={
                        "position": "absolute",
                        "left": "856px",
                        "top": "42px",
                        "backgroundColor": "transparent",
                        "border": "none",
                        
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "22px",
                        "cursor": "pointer"
                    })
                ])
            ]
        ),
        
        # Fade Dropdown for models
        dbc.Fade(
            id="model-fade",
            is_in=False,
            appear=True,
            children=html.Div(
                className="mega-dropdown",
                children=[
                    html.Div("Explore Models", className="dropdown-item-normal"),
                    dcc.Link("Model 1", href="/model1", className="dropdown-item-bold"),
                    dcc.Link("Model 2", href="/model2", className="dropdown-item-bold"),
                    dcc.Link("Model 3", href="/model3", className="dropdown-item-bold"),
                    dcc.Link("Model 4", href="/model4", className="dropdown-item-bold"),
                    dcc.Link("Compare Models", href="/comparemodels", className="dropdown-item-comparemodels")
                ]
            )
        ),
        
        # Fade Dropdown for indicators
        dbc.Fade(
            id="indicator-fade",
            is_in=False,
            appear=True,
            children=html.Div(
                className="mega-dropdown",
                children=[
                    html.Div("Explore Indicators", className="dropdown-item-normal"),
                    dcc.Link("CPI", href="/cpi", className="dropdown-item-bold"),
                    dcc.Link("Housing Stats", href="/housing", className="dropdown-item-bold"),
                    dcc.Link("PMI", href="/pmi", className="dropdown-item-bold")
                ]
            )
         ),
        
        # Main content container (where dynamic pages will be rendered)
        html.Div(id="page-content", style={"padding": "20px"})
    ]
)

# Callback to toggle indicator and model dropdown visibility and blur content
@dash.callback(
    Output("model-fade", "is_in"),
    Output("indicator-fade", "is_in"),
    Output("main-content", "style"),
    Input("model-fade-button", "n_clicks"),
    Input("indicator-fade-button", "n_clicks"),
    State("model-fade", "is_in"),
    State("indicator-fade", "is_in"),
    State("main-content", "style"),
    prevent_initial_call=True  # Avoid errors on page load
)
def toggle_fades(model_clicks, indicator_clicks, model_is_in, indicator_is_in, style):

    ctx = dash.callback_context

    # Default fallback if style is None
    if style is None:
        style = {"position": "absolute", "top": "150px", "left": "150px", "width": "300px", "filter": "none"}

    new_style = style.copy()

    if not ctx.triggered:
        return model_is_in, indicator_is_in, new_style

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "model-fade-button":
        model_show = not model_is_in
        indicator_show = False
        new_style["filter"] = "blur(5px)" if model_show else "none"
        return model_show, indicator_show, new_style

    elif triggered_id == "indicator-fade-button":
        indicator_show = not indicator_is_in
        model_show = False
        new_style["filter"] = "blur(5px)" if indicator_show else "none"
        return model_show, indicator_show, new_style

    return model_is_in, indicator_is_in, new_style