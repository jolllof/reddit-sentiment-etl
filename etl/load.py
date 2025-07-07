# TODO: define valid PK/ID for table
import pandas as pd
import psycopg2
import structlog
from psycopg2.extras import execute_values


class RedditLoader:
    def __init__(self, db_config):

        self.logger = structlog.get_logger()
        self.logger = self.logger.bind(module="load")
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def select_data(self, table_name):
        """
        Select data from PostgreSQL table.
        """
        self.logger.info(f"Selecting data from table: {table_name}")
        query = f"SELECT * FROM {table_name}"
        self.logger.info(f"Executing query: {query}")
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(data, columns=columns)
        self.logger.info(f"Data fetched: {df.head()}")
        return df

    def load_data(self, df, table_name):
        """
        Load DataFrame into PostgreSQL table.
        """
        self.logger.info(f"Loading data into table: {table_name}")

        # Ensure the DataFrame is not empty
        columns = list(df.columns)
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s ON CONFLICT (id) DO NOTHING"

        # Use execute_values for bulk insert
        execute_values(self.cursor, query, df.values)
        self.conn.commit()

        self.select_data(table_name)

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


# psql -h sentiment-db.cduosoywqqup.us-east-2.rds.amazonaws.com -U reddit_etl -d postgres -c "SELECT * FROM sentiment_data LIMIT 10;"


# psql -h <endpoint> -U <username> -p <password> <database> -c "SELECT DISTINCT tablename FROM pg_tables WHERE schemaname = 'public';"
