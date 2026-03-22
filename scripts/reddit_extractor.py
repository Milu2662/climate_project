import requests
import json
from datetime import datetime

headers = {
    "User-Agent": "python:climate.project:v1.0 (by /u/testuser)"
}

url = "https://api.reddit.com/r/climatechange?limit=100"

response = requests.get(url, headers=headers)

# Debug importante
print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))

if response.status_code != 200:
    print("Error:", response.text)
    exit()

data = response.json()

posts = data["data"]["children"]

clean_posts = []

for p in posts:
    info = p["data"]

    clean_posts.append({
        "title": info["title"],
        "text": info.get("selftext", ""),
        "score": info["score"],
        "num_comments": info["num_comments"],
        "date": info["created_utc"]
    })

filename = f"datalake_bronze/reddit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

with open(filename, "w") as f:
    json.dump(clean_posts, f, indent=4)

print(f"✅ {len(clean_posts)} posts guardados")