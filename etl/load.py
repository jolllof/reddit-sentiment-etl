
#TODO: define valid PK/ID for table
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd


class RedditLoader():
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def load_data(self, df, table_name):
        """
        Load DataFrame into PostgreSQL table.
        """
        columns = list(df.columns)
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
        
        # Use execute_values for bulk insert
        execute_values(self.cursor, query, df.values)
        self.conn.commit()

    def close(self):
        """
        Close database connection.
        """
        self.cursor.close()
        self.conn.close()

# Load Phase
# Database Design:

# Decide on storage: relational DB (PostgreSQL), NoSQL (MongoDB), or data warehouse (BigQuery, Snowflake)
# Design schema with proper indexing for your analysis queries
# Consider partitioning by date or subreddit for performance


#psql -h sentiment-db.cduosoywqqup.us-east-2.rds.amazonaws.com -U reddit_etl -d sentiment_etl -p 5432
