from dash import html, register_page

register_page(__name__, path="/model1", name="Model 1")

layout = html.Div([
    html.H1("Model 1 Page"),
])