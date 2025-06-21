# tweet-sentiment-etl
an automated ETL pipeline that extracts trending topics, gathers related tweets, performs text cleaning and sentiment analysis.
# Trending Tweets Sentiment ETL Pipeline

## Overview

This project demonstrates an **automated ETL pipeline** that extracts trending topics from Twitter (X), gathers related tweets, performs **text cleaning and sentiment analysis**, and stores the enriched data in a structured format. The pipeline is fully orchestrated using **Apache Airflow** and can scale with **PySpark** for large datasets.

---

## Key Features

-  **Data Extraction:** Collects real-time trending topics and sample tweets using the Twitter API.
-  **Data Transformation:** Cleans tweet text (removes URLs, emojis, mentions, etc.) and filters for relevance and language.
-  **Sentiment Enrichment:** Classifies each tweet as *Positive*, *Negative*, or *Neutral* using **VADER Sentiment Analysis** (or optional BERT model).
-  **Data Loading:** Stores processed data into **AWS S3** (or local storage), optionally loads into a **PostgreSQL/BigQuery** warehouse.
-  **Orchestration:** Managed by **Apache Airflow DAG**, with configurable schedules (e.g., every 6 hours).

---


