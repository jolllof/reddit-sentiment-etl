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
  Cleans post content (removes URLs, emojis, markdown formatting, etc.) and filters for language and relevance. **NLTK** for tokenization, stopwords, word lemmatizing and ***TextBlob** to fix typos

- **🧠 Sentiment Enrichment**
  Classifies each post as *Positive*, *Negative*, or *Neutral* using the RoBERTA based transformer **cardiffnlp/twitter-roberta-base-sentiment** and emotion classification using  **j-hartmann/emotion-english-distilroberta-base**. Additionally **scikit-learn** is implemented for tone clustering.

- **📦 Data Loading**
  Writes results to **AWS RDS** table and saves processed data to **AWS S3**.

- **⏱ Orchestration**
  Workflow is scheduled and managed using **Apache Airflow DAGs**, with customizable run intervals (e.g., hourly or daily).

---

## 🛠 Technologies Used

- Python 3
- PRAW (Python Reddit API Wrapper)
- NLTK
- Pandas
- Sentiment Transformer (cardiffnlp/twitter-roberta-base-sentiment)
- Emotion Transformer (j-hartmann/emotion-english-distilroberta-base)
- Scikit-Learn
- Apache Airflow
- PySpark (optional for scale)
- AWS S3 / RDS / PostgreSQL
- TQDM progressbars

---

## ✅ Next Steps

- Deploy with Docker and set up on a cloud scheduler (e.g., AWS MWAA or Cloud Composer)

---

## 📬 Contact

Feel free to reach out or open an issue for questions or collaboration ideas at: **jollofcodes@gmail.com**
