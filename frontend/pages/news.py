import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash 
from dash import html, dcc, Input, Output, State

API_KEY = "2b46d4bf36014684bb695c54fe6107b9"
url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",
    "category": "business",
    "pageSize": 10, # Number of articles to return
    "apiKey": API_KEY
}


response = requests.get(url, params=params)
data = response.json()

articles = data.get("articles", [])

# Optional: extract source name from nested dict
for article in articles:
    if "source" in article and isinstance(article["source"], dict):
        article["source"] = article["source"].get("name")

df_articles = pd.DataFrame(articles)
#print(df_articles[["title", "source", "url", "urlToImage"]])

def generate_card_scroll(df):
    return html.Div(
        style={
            "height": "600px",
            "overflowY": "auto",
            "padding": "10px",
            "backgroundColor": "transparent",
            "maxWidth": "100%",
            "overflowX": "hidden"
        },
        children=[
            dbc.Card(
                children=[
                    dbc.CardImg(src=row["urlToImage"], top=True),
                    dbc.CardBody([
                        html.A(row["title"], href=row["url"], className="card-title", target="_blank")
                    ])
                ],
                style={
                    "left": "35px",
                    "overflowY": "auto",
                    "overflowX": "hidden",
                    "marginBottom": "20px",
                    "backgroundColor": "#1a1a1a",
                    "border": "1px solid #444",
                    "borderRadius": "10px",
                    "maxWidth": "100%"
                }
            )
            for _, row in df.iterrows()
            if row["urlToImage"]  # skip if no image
        ]
    )

