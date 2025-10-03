import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of Malayalam news sites (home/news pages)
news_sites = {
    "Onmanorama": "https://www.onmanorama.com/news.html",
    "Mathrubhumi": "https://www.mathrubhumi.com/english/news",
    "Manorama": "https://www.manoramaonline.com/news/latest-news.html"
}

articles = []

def scrape_onmanorama(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for item in soup.find_all("a", class_="cmp-story-list__title-link"):
        title = item.get_text(strip=True)
        link = item.get("href")
        if not link.startswith("http"):
            link = "https://www.onmanorama.com" + link
        # Fetch article text
        article_text = fetch_article_text(link, ["p"])
        if article_text:
            articles.append({"title": title, "text": article_text, "label": "REAL"})

def scrape_mathrubhumi(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for item in soup.find_all("a", class_="no-underline content-font"):
        title = item.get_text(strip=True)
        link = item.get("href")
        if not link.startswith("http"):
            link = "https://www.mathrubhumi.com" + link
        article_text = fetch_article_text(link, ["p"])
        if article_text:
            articles.append({"title": title, "text": article_text, "label": "REAL"})

def scrape_manorama(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for item in soup.find_all("a", class_="cmp-story-list__title-link"):
        title = item.get_text(strip=True)
        link = item.get("href")
        if not link.startswith("http"):
            link = "https://www.manoramaonline.com" + link
        article_text = fetch_article_text(link, ["p"])
        if article_text:
            articles.append({"title": title, "text": article_text, "label": "REAL"})

def fetch_article_text(link, tags):
    try:
        res = requests.get(link, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = []
        for tag in tags:
            for p in soup.find_all(tag):
                paragraphs.append(p.get_text(strip=True))
        return " ".join(paragraphs)
    except:
        return ""

# Scrape each site
print("Scraping Onmanorama...")
scrape_onmanorama(news_sites["Onmanorama"])
time.sleep(2)

print("Scraping Mathrubhumi...")
scrape_mathrubhumi(news_sites["Mathrubhumi"])
time.sleep(2)

print("Scraping Manorama Online...")
scrape_manorama(news_sites["Manorama"])
time.sleep(2)

# Save to CSV
df = pd.DataFrame(articles)
df.to_csv("malayalam_news_real.csv", index=False)
print(f"Scraping done! {len(articles)} articles saved to malayalam_news_real.csv")


