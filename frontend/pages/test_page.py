import dash
from dash import html, dcc
from shared.default_pagelayout import get_default_layout 


dash.register_page(__name__, path="/test_page", name="Housing Starts")

# Define the custom content you want in the main area
test_content = html.Div(
    id="main-content",
    style={
        "position": "absolute",
        "top": "120px",
        "left": "65px",
        "width": "600px",
        # etc. 
    },
    children=[
        html.H2("CPI Nowcasting", style={"color": "white"}),
        # your graphs, tables, etc.
    ]
)

# Plug that content into your default layout
layout = get_default_layout(main_content=test_content)
