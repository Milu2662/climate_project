from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from datetime import datetime
import os
import json
import pandas as pd

BRONZE_PATH = "/opt/airflow/datalake_bronze"
SILVER_PATH = "/opt/airflow/datalake_silver"

@dag(
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["silver", "climate"]
)
def silver_processing():

    # Sensor: espera archivos en Bronze
    wait_for_file = FileSensor(
        task_id="wait_for_bronze_file",
        filepath=BRONZE_PATH,
        poke_interval=30,
        timeout=300,
        mode="poke"
    )

    @task
    def process_data():
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            import nltk

            # Asegura que VADER esté disponible
            nltk.download('vader_lexicon')

            sia = SentimentIntensityAnalyzer()

            # Solo archivos de Reddit (evita errores con news)
            files = [
                f for f in os.listdir(BRONZE_PATH)
                if f.startswith("reddit_") and f.endswith(".json")
            ]

            if not files:
                print("No files found in Bronze")
                return

            # Toma el archivo más reciente
            latest_file = sorted(files)[-1]
            filepath = os.path.join(BRONZE_PATH, latest_file)

            with open(filepath, "r") as f:
                data = json.load(f)

            records = []

            # Manejo seguro del JSON
            for post in data.get("data", {}).get("children", []):
                title = post.get("data", {}).get("title", "")
                text = post.get("data", {}).get("selftext", "")

                combined_text = f"{title} {text}"

                sentiment = sia.polarity_scores(combined_text)["compound"]

                if sentiment >= 0.05:
                    label = "positive"
                elif sentiment <= -0.05:
                    label = "negative"
                else:
                    label = "neutral"

                records.append({
                    "text": combined_text,
                    "sentiment_score": sentiment,
                    "label": label
                })

            if not records:
                print("No valid records found")
                return

            df = pd.DataFrame(records)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"sentiment_{timestamp}.parquet"

            output_path = os.path.join(SILVER_PATH, output_file)

            df.to_parquet(output_path)

            print(f"Parquet saved successfully at {output_path}")

        except Exception as e:
            print(f"Error during processing: {e}")

    # Flujo del DAG
    wait_for_file >> process_data()

# Instancia del DAG
dag = silver_processing()
