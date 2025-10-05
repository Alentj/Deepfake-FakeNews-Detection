from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import requests, re
from transformers import pipeline

app = Flask(__name__)

# ------------------ Deepfake model ------------------
MODEL_PATH = "deepfake_cnn_model(train only).h5"
model = load_model(MODEL_PATH)
class_names = ["Real", "Fake"]

# ------------------ Fake news model ------------------
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", framework="pt")

# ------------------ API KEYS ------------------
NEWSAPI_KEY = "4924e0ad7a214971b8f623bebb0b5f22"
NEWSDATA_KEY = "pub_8c90793db2b744669a7af65ceadef653"
MEDIASTACK_KEY = "ba5eef4a21fd1259d5d6549ce9d6c986"
GNEWS_KEY = "1a8bd1c7d5bd2d677e3d96eec40f7f52"
BING_KEY = "BFCSNfOCNX5CYNGGAJnKvF5XN622fk3CIsjL5qODYmAzSeCsY26x"
NYT_KEY = "575assfdtIz6DlKqPp2gaG09b3jiQ3mL"
GUARDIAN_KEY = "25c6f980-501c-4c9f-b7aa-2185c8e803c5"
CURRENTS_KEY = "BLvLO599ACcjFbJM45T3og2m6nHOGbCtq6_gU_nLXfzNV50h"

# ------------------ TEXT CLEANING ------------------
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text)
    return text.lower()

def predict_fake_news(text):
    text = clean_text(text)
    labels = ["FAKE", "REAL"]
    result = classifier(text, candidate_labels=labels)
    return {"label": result["labels"][0], "score": result["scores"][0]}

# ------------------ NEWS FETCH FUNCTIONS ------------------
def fetch_news_newsapi(query, max_results=5):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={max_results}&apiKey={NEWSAPI_KEY}"
    data = requests.get(url).json()
    news_list = []
    for article in data.get("articles", []):
        news_list.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source", {}).get("name"),
            "url": article.get("url")
        })
    return news_list

def fetch_news_gnews(query, max_results=5):
    url = f"https://gnews.io/api/v4/search?q={query}&token={GNEWS_KEY}&max={max_results}"
    data = requests.get(url).json()
    news_list = []
    for article in data.get("articles", []):
        news_list.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source", {}).get("name"),
            "url": article.get("url")
        })
    return news_list

def fetch_news_mediastack(query, max_results=5):
    url = f"http://api.mediastack.com/v1/news?access_key={MEDIASTACK_KEY}&keywords={query}&limit={max_results}"
    data = requests.get(url).json()
    news_list = []
    for article in data.get("data", []):
        news_list.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source"),
            "url": article.get("url")
        })
    return news_list

def fetch_news_bing(query, max_results=5):
    url = f"https://api.bing.microsoft.com/v7.0/news/search?q={query}&count={max_results}"
    headers = {"Ocp-Apim-Subscription-Key": BING_KEY}
    data = requests.get(url, headers=headers).json()
    news_list = []
    for article in data.get("value", []):
        news_list.append({
            "title": article.get("name"),
            "description": article.get("description"),
            "source": article.get("provider")[0].get("name") if article.get("provider") else None,
            "url": article.get("url")
        })
    return news_list

def fetch_news_nyt(query, max_results=5):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={NYT_KEY}"
    data = requests.get(url).json()
    news_list = []
    for article in data.get("response", {}).get("docs", [])[:max_results]:
        news_list.append({
            "title": article.get("headline", {}).get("main"),
            "description": article.get("abstract"),
            "source": "NYTimes",
            "url": article.get("web_url")
        })
    return news_list

def fetch_news_guardian(query, max_results=5):
    url = f"https://content.guardianapis.com/search?q={query}&api-key={GUARDIAN_KEY}&page-size={max_results}&show-fields=trailText"
    data = requests.get(url).json()
    news_list = []
    for article in data.get("response", {}).get("results", []):
        news_list.append({
            "title": article.get("webTitle"),
            "description": article.get("fields", {}).get("trailText"),
            "source": "The Guardian",
            "url": article.get("webUrl")
        })
    return news_list

def fetch_news_currents(query, max_results=5):
    url = f"https://api.currentsapi.services/v1/search?keywords={query}&apiKey={CURRENTS_KEY}&limit={max_results}"
    data = requests.get(url).json()
    news_list = []
    for article in data.get("news", []):
        news_list.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("author"),
            "url": article.get("url")
        })
    return news_list

def fetch_all_news(query):
    functions = [
        fetch_news_newsapi,
        fetch_news_gnews,
        fetch_news_mediastack,
        fetch_news_bing,
        fetch_news_nyt,
        fetch_news_guardian,
        fetch_news_currents
    ]
    all_news = []
    for func in functions:
        try:
            items = func(query)
            for item in items:
                item["prediction"] = predict_fake_news((item["title"] or "") + " " + str(item.get("description", "")))
                all_news.append(item)
        except Exception as e:
            print(f"Error fetching news from {func.__name__}: {e}")
    return all_news

# ------------------ ROUTES ------------------
@app.route("/", methods=["GET", "POST"])
def dashboard():
    results = []
    if request.method == "POST":
        query = request.form.get("query")
        results = fetch_all_news(query)
    return render_template("dashboard.html", results=results)

@app.route("/predict", methods=["POST"])
def predict_deepfake():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    img = cv2.resize(img, (128,128))/255.0
    img = img.reshape(1,128,128,3)
    prediction = model.predict(img)
    pred_index = np.argmax(prediction)
    confidence = float(np.max(prediction)) * 100
    pred_label = class_names[pred_index]
    return jsonify({"prediction": pred_label, "confidence": f"{confidence:.2f}%"})

if __name__ == "__main__":
    app.run(debug=True)


