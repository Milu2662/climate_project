import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.theguardian.com/environment"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("a", href=True)

data = []

for a in articles:
    title = a.get_text(strip=True)
    link = a.get("href")


    if link and "/202" in link and len(title) > 40:

        # 🔥 URL completa
        if link.startswith("/"):
            link = "https://www.theguardian.com" + link

        try:
            article_page = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_page.text, "html.parser")

            paragraphs = article_soup.find_all("p")
            content = " ".join([p.get_text() for p in paragraphs])

            if len(content) > 100:
                data.append({
                    "title": title,
                    "url": link,
                    "content": content[:1000]
                })

            time.sleep(0.5)

        except Exception as e:
            print("Error:", e)

filename = f"datalake_bronze/news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=4)

print(f"✅ {len(data)} artículos guardados")