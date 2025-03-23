from dash import html
import dash_bootstrap_components as dbc

def get_fade_component():
    return html.Div(
        [
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(
                        html.P("This content fades in and out", className="card-text")
                    )
                ),
                id="fade",
                is_in=False,
                appear=True,
            ),
        ],
        id="fade-container",
        style={"position": "absolute", "top": "150px", "left": "75px", "width": "300px"}
    )
