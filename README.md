# Climate Change Data Pipeline

## Overview
This project implements a data pipeline using Apache Airflow following the Medallion Architecture.

## Architecture
- Bronze: Raw JSON data from Reddit API
- Silver: Processed data with sentiment analysis (Parquet)

## Tech Stack
- Python
- Apache Airflow
- Docker
- Pandas
- NLTK

## Setup Instructions

### Run Docker
docker compose up

### Access Airflow
http://localhost:8080

### Run DAGs
- Enable bronze_ingestion
- Enable silver_processing

## Repository Structure
- airflow/dags/
- datalake_bronze/
- datalake_silver/
- workshop_2
