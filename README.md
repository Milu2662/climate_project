# Climate Change Data Pipeline

# Overview

This project implements a data engineering pipeline to analyze public opinion on climate change using sentiment analysis.

The pipeline follows the Medallion Architecture (Bronze and Silver layers) and is orchestrated using Apache Airflow within a Docker environment.

Data is collected from Reddit, processed using Natural Language Processing (NLP), and stored in structured formats for analysis.

⸻

# Architecture

The pipeline is composed of the following layers:
	•	Bronze Layer: Raw JSON data from Reddit API
	•	Silver Layer: Processed data with sentiment analysis (Parquet format)
	•	Gold Layer (future work): Aggregated analytical data
	•	Visualization (future work): Dashboard for insights

⸻

️# Tech Stack
	•	Python
	•	Apache Airflow
	•	Docker & Docker Compose
	•	Pandas
	•	NLTK (VADER Sentiment Analysis)
	•	Parquet (PyArrow)

⸻

# How to Run the Project

1. Clone the repository
	git clone https://github.com/Milu2662/climate_project.git
	cd climate_project
2. Start Docker services
	docker compose up
3. Access Airflow

Open in your browser: http://localhost:8080

Credentials:
	•	Username: airflow
	•	Password: airflow

4. Run the Pipeline
	1.	Activate DAGs:
		bronze_ingestion
		silver_processing
	2.	Execute:
		First run Bronze DAG
		Then run Silver DAG
# Pipeline Description

# Bronze Ingestion DAG
	Extracts data from Reddit API
	Validates JSON structure
	Stores raw data in:		datalake_bronze/
	File format:	reddit_YYYYMMDD_HHMMSS.json
# Silver Processing DAG
	Uses FileSensor to detect new Bronze files
	Loads JSON data
	Combines text fields (title + content)
	Applies sentiment analysis using VADER
	Stores processed data in:	datalake_silver/
		File format:	sentiment_YYYYMMDD_HHMMSS.parquet


⸻

# Data Exploration
A Jupyter Notebook is included:	notebooks/explore_data.ipynb
It demonstrates:
	Reading Parquet files
	Inspecting data structure
	Sentiment distribution analysis

⸻

# Project Structure
climate_project/
│
├── airflow/
│   └── dags/
│       ├── bronze_ingestion_dag.py
│       └── silver_processing_dag.py
│
├── datalake_bronze/
├── datalake_silver/
├── datalake_gold/
│
├── notebooks/
│   └── explore_data.ipynb
│
├── workshop_2/
│   └── report.pdf
│
├── docker-compose.yml
├── requirements.txt
└── README.md


⸻

# Results

The pipeline successfully:
	Executes automated workflows using Airflow
	Generates JSON files in the Bronze layer
	Produces Parquet files in the Silver layer
	Applies sentiment analysis to textual data
	Allows data exploration using Pandas

⸻

# Challenges

	Configuring Airflow within Docker environment
	Managing dependencies (NLTK, PyArrow)
	Handling different data structures from sources
	Ensuring file detection using FileSensor

⸻

# Future Work

	Implement Gold layer (aggregations)
	Add dashboard (Plotly / Power BI)
	Improve NLP model (ML / Deep Learning)
	Expand data sources

⸻

# Authors

	Luisa Fernanda Guerrero Ordoñez
	Luisa Fernanda Velasco López
	Daniel Alejandro Presiga Presiga
