import requests

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

for article in data["articles"]:
    print(article["title"], article["urlToImage"])
