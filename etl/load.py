from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd

# Set your local file path here
CSV_FILE_PATH = '/path/to/sentiment_data.csv'

def load_csv_to_postgres():
    # Read the CSV
    df = pd.read_csv(CSV_FILE_PATH)

    # Clean: Convert boolean and timestamp fields
    df['nsfw'] = df['nsfw'].astype(bool)
    df['created_utc'] = pd.to_datetime(df['created_utc'])
    df['extracted_at'] = pd.to_datetime(df['extracted_at'])

    # Connect to Postgres
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    engine = pg_hook.get_sqlalchemy_engine()

    # Load into table (replace 'reddit_sentiment' with your table name)
    df.to_sql('reddit_sentiment', engine, if_exists='append', index=False)

# Define the DAG
with DAG(
    dag_id='load_sentiment_to_postgres',
    start_date=datetime(2025, 7, 1),
    schedule_interval=None,  # Run manually or on trigger
    catchup=False,
    tags=['reddit', 'sentiment', 'postgres']
) as dag:

    load_task = PythonOperator(
        task_id='load_csv_to_pg',
        python_callable=load_csv_to_postgres
    )

    load_task


# Load Phase
# Database Design:

# Decide on storage: relational DB (PostgreSQL), NoSQL (MongoDB), or data warehouse (BigQuery, Snowflake)
# Design schema with proper indexing for your analysis queries
# Consider partitioning by date or subreddit for performance
