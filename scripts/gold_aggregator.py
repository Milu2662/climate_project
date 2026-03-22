import pandas as pd

df = pd.read_parquet("datalake_silver/data.parquet")


summary = df.groupby("label").size().reset_index(name="count")


avg_sentiment = df["sentiment_score"].mean()


summary.to_csv("datalake_gold/sentiment_summary.csv", index=False)

with open("datalake_gold/metrics.txt", "w") as f:
    f.write(f"Average Sentiment: {avg_sentiment}")

print("✅ Gold generado")