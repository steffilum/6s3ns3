import dash
from dash import html
import dash_bootstrap_components as dbc
import shared.navbar_callback 

app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="pages", 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

app.layout = html.Div([
    dash.page_container  # renders the correct registered page
])

if __name__ == "__main__":
    app.run(debug=True)
