import requests
import pandas as pd

API_KEY = "2b46d4bf36014684bb695c54fe6107b9"
url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",
    "category": "business",
    "pageSize": 5, # Number of articles to return
    "apiKey": API_KEY
}


response = requests.get(url, params=params)
data = response.json()

articles = data.get("articles", [])

# Optional: extract source name from nested dict
for article in articles:
    if "source" in article and isinstance(article["source"], dict):
        article["source"] = article["source"].get("name")

df = pd.DataFrame(articles)
print(df[["title", "source", "url", "urlToImage"]])
