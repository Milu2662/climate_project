import pandas as pd
import json
import glob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

files = glob.glob("datalake_bronze/*.json")

data = []

for file in files:
    with open(file) as f:
        content = json.load(f)

        for item in content:
            text = item.get("title", "") + " " + item.get("text", "") + " " + item.get("content", "")

            if text.strip():

                score = sia.polarity_scores(text)["compound"]

                if score >= 0.05:
                    label = "positive"
                elif score <= -0.05:
                    label = "negative"
                else:
                    label = "neutral"

                data.append({
                    "text": text,
                    "sentiment_score": score,
                    "label": label
                })

df = pd.DataFrame(data)

df.to_parquet("datalake_silver/data.parquet")

print(f"✅ {len(df)} registros procesados")