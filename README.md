# reddit-sentiment-etl

An automated ETL pipeline that extracts hot posts from Reddit, cleans text, performs natural language processing, sentiment analysis, and stores enriched data.

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
  Cleans post content (removes URLs, emojis, markdown formatting, etc.) and filters for language and relevance. **NLTK** for tokenization and stopwords, ***TextBlob** to fix typos

- **🧠 Sentiment Enrichment**  
  Classifies each post as *Positive*, *Negative*, or *Neutral* using **RoBERTA Sentiment Analysis**, with optional support for transformer models like **BERT**.

- **📦 Data Loading**  
  Saves processed data to **AWS S3** or local storage. Optionally supports loading into **PostgreSQL** or **BigQuery** for querying.

- **⏱ Orchestration**  
  Workflow is scheduled and managed using **Apache Airflow DAGs**, with customizable run intervals (e.g., hourly or daily).

---

## 🛠 Technologies Used

- Python 3
- PRAW (Python Reddit API Wrapper)
- NLTK
- Pandas
- RoBERTA (cardiffnlp/twitter-roberta-base-sentiment)
- Apache Airflow
- PySpark (optional for scale)
- AWS S3 / PostgreSQL / BigQuery (optional for storage)

---

## ✅ Next Steps

- Add topic modeling or keyword extraction
- Incorporate comment sentiment for deeper insights
- Deploy with Docker and set up on a cloud scheduler (e.g., AWS MWAA or Cloud Composer)

---

## 📬 Contact

Feel free to reach out or open an issue for questions or collaboration ideas!
