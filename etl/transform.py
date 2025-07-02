import structlog
import pandas as pd
from utilities import save_posts_to_csv
from config.config import load_yaml_config
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob




# Uncomment the following lines if you need to download NLTK data files
#import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# nltk.download('punkt', quiet=True, download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')
# nltk.download('punkt_tab', download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')
# nltk.download('wordnet', download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')
# nltk.download('omw-1.4', download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')



class RedditTransformer:
    """
    Class to transform raw Reddit data into a structured format.
    """

    def __init__(self):
        self.logger = structlog.get_logger()
        self.logger = self.logger.bind(module="transform")
        self.current_datetime = datetime.now()


    def text_cleanup(self, df):
        """
        Perform basic text cleaning on the DataFrame.
        :param df: Pandas DataFrame containing Reddit post data.
        :return: DataFrame with cleaned text data.
        """
        
        self.logger.info("Starting Basic Text Cleaning")
     
        # Perform necessary transformations
        df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
        df.drop(columns=['url'], inplace=True, errors='ignore')

        # Clean text data
        df['title'] = df['title'].str.replace(r'http\S+|www\S+|https\S+', '', regex=True)  # Remove URLs
        df['title'] = df['title'].str.replace(r'[^\w\s]', '', regex=True)  # Remove special characters
        df['title'] = df['title'].str.lower()  # Convert to lowercase
        df['title'] = df['title'].str.strip()  # Remove leading/trailing whitespace
        df['title'] = df['title'].str.replace(r'\s+', ' ', regex=True)  # Normalize whitespace
        df['title'] = df['title'].str.replace(r'\b\w{1,2}\b', '', regex=True)  # Remove short words

        return df

    def fix_typos(self, df):
        """
        Fix common typos in the DataFrame.
        
        :param  
        df: Pandas DataFrame containing text data.
        :return: DataFrame with fixed typos.
        """ 
        df['title'] = df['title'].apply(lambda x: str(TextBlob(x).correct()))
        self.logger.info("Fixed typos in text data")
        return df

    def tokenization(self, df):
        """
        Tokenizes the text data in the DataFrame.
        
        :param
        df: Pandas DataFrame containing text data.
        :return: DataFrame with tokenized text.
        """
    
        self.logger.info("Tokenizing and removing stop words")
        
        self.logger.info(f"Loading keepwords from config")
        keepwords = load_yaml_config('keep_words')

        default_stopwords = set(stopwords.words('english'))
        stopwords_combined = default_stopwords - set(keepwords) 

        df['tokens'] = df['title'].apply(
            lambda x: [word for word in word_tokenize(x) if word not in stopwords.words('english') and word not in keepwords]                                                   
        )

        return df

    def transform_data(self, df, save_to_csv=True):
        """
        Transforms raw Reddit data into a structured DataFrame.
        
        :param raw_data: List of dictionaries containing raw Reddit post data.
        :return: Pandas DataFrame with transformed data.
        """
        
        df = self.text_cleanup(df)
        df = self.fix_typos(df)
        df = self.tokenization(df)
        
        
        # Log the shape of the DataFrame after transformation
        self.logger.info(f"Transformed data shape: {df.shape}")

         # Save to CSV if requested
        if save_to_csv:
            filename=save_posts_to_csv(df, current_datetime=self.current_datetime, filename="transformed")
        
        return df
    








#     For the transform and load portions of your Reddit ETL sentiment analysis pipeline, here are the key next steps:
# Transform Phase
# Data Cleaning & Preprocessing:

# Remove deleted/removed posts and comments
# Handle missing values and duplicates
# Clean text data (remove URLs, special characters, normalize whitespace)
# Filter out bot accounts and spam content
# Standardize datetime formats

# Text Preprocessing for Sentiment Analysis:

# Tokenization and lowercasing
# Remove stop words (but be careful - some like "not" are crucial for sentiment)
# Handle negations properly
# Consider lemmatization/stemming
# Deal with Reddit-specific elements (subreddit mentions, user tags, markdown)

# Sentiment Analysis Implementation:

# Choose your approach: rule-based (VADER), pre-trained models (TextBlob, spaCy), or transformer models (BERT, RoBERTa)
# Consider Reddit-specific sentiment models if available
# Generate sentiment scores (positive, negative, neutral, compound)
# Add confidence scores if your model supports them

# Feature Engineering:

# Extract metadata features (post length, comment count, upvote ratio)
# Time-based features (hour of day, day of week, seasonality)
# Subreddit categorization
# User engagement metrics

# Load Phase
# Database Design:

# Decide on storage: relational DB (PostgreSQL), NoSQL (MongoDB), or data warehouse (BigQuery, Snowflake)
# Design schema with proper indexing for your analysis queries
# Consider partitioning by date or subreddit for performance

# Data Pipeline Architecture:

# Batch processing (Apache Airflow, Prefect) vs streaming (Apache Kafka, AWS Kinesis)
# Error handling and data validation
# Monitoring and alerting for pipeline failures

# What's your current data volume and how frequently do you plan to update the analysis? This will help determine the best architecture approach.