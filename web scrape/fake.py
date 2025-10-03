import pandas as pd
from googletrans import Translator
import time

# Load Excel file
df = pd.read_excel("liar_data.xlsx")

# Convert columns to lowercase for convenience
df.columns = [col.lower() for col in df.columns]

# Check columns
print(df.columns)
print(df.head())

# Map LIAR labels to FAKE / REAL
label_map = {
    "FALSE": "FAKE",
    "PANTS-FIRE": "FAKE",
    "TRUE": "REAL",
    "MOSTLY-TRUE": "REAL",
    "HALF-TRUE": "REAL"
}

df['label'] = df['label'].map(label_map)

# Keep only FAKE for translation
df_fake = df[df['label'] == 'FAKE'][['text','label']]

# Initialize translator
translator = Translator()
malayalam_texts = []

for text in df_fake['text']:
    try:
        translated = translator.translate(text, src='en', dest='ml').text
        malayalam_texts.append(translated)
        time.sleep(0.5)  # avoid rate limits
    except:
        malayalam_texts.append("")  # fallback if translation fails

df_fake['text_ml'] = malayalam_texts
df_fake['label'] = 'FAKE'  # ensure label remains FAKE

# Save translated dataset
df_fake[['text_ml','label']].to_csv("liar_fake_malayalam.csv", index=False)
print("Translation done! Saved to liar_fake_malayalam.csv")

# Load REAL Malayalam news
df_real_ml = pd.read_csv("malayalam_news_real.csv")  # your scraped REAL news
df_fake_ml = pd.read_csv("liar_fake_malayalam.csv")  # translated FAKE news

# Combine datasets
df_all = pd.concat([df_real_ml, df_fake_ml], ignore_index=True)
df_all.to_csv("news_dataset.csv", index=False)
print(f"Final multilingual dataset ready! Total size: {len(df_all)}")
