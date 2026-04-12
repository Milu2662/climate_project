from airflow.decorators import dag, task
from datetime import datetime
import requests
import json
import os

BRONZE_PATH = "/opt/airflow/datalake_bronze"

@dag(
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["bronze", "climate"]
)
def bronze_ingestion():

    @task
    def extract_reddit():
        url = "https://www.reddit.com/r/climatechange.json"
        headers = {"User-Agent": "airflow-pipeline"}

        response = requests.get(url, headers=headers)
        data = response.json()

        return data

    @task
    def save_data(data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reddit_{timestamp}.json"

        filepath = os.path.join(BRONZE_PATH, filename)

        with open(filepath, "w") as f:
            json.dump(data, f)

        return filepath

    data = extract_reddit()
    save_data(data)

dag = bronze_ingestion()
