import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from dash import page_container

# Import layout
from layout import layout

# Create the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # You can customize your theme here
    use_pages=True,  # Enables Dash's native multi-page support
    suppress_callback_exceptions=True
)

server = app.server

# App layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Keeps track of the URL
    layout,
    page_container  # Where the pages will be rendered dynamically
])

# Run the server if this file is executed directly
if __name__ == "__main__":
    app.run_server(debug=True)
