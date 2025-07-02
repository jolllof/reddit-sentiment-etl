# reddit-sentiment-etl

An automated ETL pipeline that extracts hot posts from Reddit, cleans text, performs sentiment analysis, and stores enriched data.

---

## 🧠 Overview

This project demonstrates an **automated ETL pipeline** that:

- Extracts **hot posts** from selected Reddit subreddits
- Performs **text preprocessing and sentiment analysis**
- Stores the enriched data in a structured format

The pipeline will be orchestrated using **Apache Airflow** and should scale using **PySpark** for larger datasets.

---

## 🚀 Key Features

- **🔍 Data Extraction**  
  Collects hot posts from specified subreddits using the Reddit API via **PRAW**.

- **🧹 Data Transformation**  
  Cleans post content (removes URLs, emojis, markdown formatting, etc.) and filters for language and relevance.

- **🧠 Sentiment Enrichment**  
  Classifies each post as *Positive*, *Negative*, or *Neutral* using **VADER Sentiment Analysis**, with optional support for transformer models like **BERT**.

- **📦 Data Loading**  
  Saves processed data to **AWS S3** or local storage. Optionally supports loading into **PostgreSQL** or **BigQuery** for querying.

- **⏱ Orchestration**  
  Workflow is scheduled and managed using **Apache Airflow DAGs**, with customizable run intervals (e.g., hourly or daily).

---

## 🛠 Technologies Used

- Python 3
- PRAW (Python Reddit API Wrapper)
- VADER (NLTK Sentiment Analyzer)
- Apache Airflow
- PySpark (optional for scale)
- AWS S3 / PostgreSQL / BigQuery (optional for storage)

---

## 📌 Notes

- Reddit’s "hot" posts reflect trending content, which may introduce engagement or popularity bias.
- VADER is tuned for social media, but transformer models may improve accuracy for more nuanced sentiment.

---

## ✅ Next Steps

- Add topic modeling or keyword extraction
- Incorporate comment sentiment for deeper insights
- Deploy with Docker and set up on a cloud scheduler (e.g., AWS MWAA or Cloud Composer)

---

## 📬 Contact

Feel free to reach out or open an issue for questions or collaboration ideas!
