# models/sentiment.py
from transformers import pipeline
import structlog
import pandas as pd
from utilities import save_posts_to_csv
from datetime import datetime


class SentimentAnalyzer:
    """
    Class to perform sentiment and emotion analysis on text data.
    Uses Hugging Face Transformers for sentiment analysis.
    """
    def __init__(self):
        self.logger = structlog.get_logger()
        self.current_datetime = datetime.now()
        self.logger = self.logger.bind(module="sentiment")
        self.sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
        self.emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

    def analyze_sentiment(self, text):
        try:
            result = self.sentiment_model(text[:512])  # Limit input length for safety
            return result[0]['label'], float(result[0]['score'])
        except Exception as e:
            self.logger.error("Sentiment analysis failed", error=str(e))
            return "ERROR", 0.0

    def analyze_emotion(self, text):
        try:
            result = self.emotion_model(text[:512])
            return result[0]['label'], float(result[0]['score'])
        except Exception as e:
            self.logger.error("Emotion analysis failed", error=str(e))
            return "ERROR", 0.0

    # def subreddit_tone_clustering(self, df, n_clusters=5):
    #     """
    #     Perform clustering on subreddit tones based on sentiment and emotion scores.
        
    #     :param df: DataFrame containing sentiment and emotion columns.
    #     :param n_clusters: Number of clusters to form.
    #     :return: DataFrame with cluster labels added.
    #     """

    #     from sklearn.cluster import KMeans
    #     from sklearn.preprocessing import StandardScaler

    #     # Select relevant features for clustering
    #     features = df[['sentiment_confidence', 'emotion_confidence']]
        
    #     # Scale the features
    #     scaler = StandardScaler()
    #     scaled_features = scaler.fit_transform(features)

    #     # Perform KMeans clustering
    #     kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    #     df['tone_cluster'] = kmeans.fit_predict(scaled_features)

    #     self.logger.info(f"Clustering completed with {n_clusters} clusters")
        
    #     return df

    def apply_analysis(self, df, save_to_csv=False):
        """
        Applies sentiment analysis to the cleaned titles in the DataFrame.
        :param df: Pandas DataFrame containing cleaned titles.
        :return: DataFrame with sentiment labels and confidence scores.
        """
        label_map = {
            "LABEL_0": "Negative",
            "LABEL_1": "Neutral",
            "LABEL_2": "Positive"
        }
        
        self.logger.info("Applying sentiment analysis to cleaned titles")
        sentiments = df['cleaned_title'].apply(self.analyze_sentiment)
        
        df['sentiment'] = sentiments.apply(lambda x: label_map.get(x[0], x[0]))  # Map label or fallback to original
        df['sentiment_confidence'] = sentiments.apply(lambda x: x[1])

        self.logger.info("Applying emotion analysis to cleaned titles")
        emotions = df['cleaned_title'].apply(self.analyze_emotion) 
        df['emotion'] = emotions.apply(lambda x: x[0])
        df['emotion_confidence'] = emotions.apply(lambda x: x[1])

        if save_to_csv:
            save_posts_to_csv(df, current_datetime=self.current_datetime, filename="sentiment_analysis")
        return df
    
# Feature Engineering:

# Subreddit categorization
# User engagement metrics


# Data Pipeline Architecture:

# Batch processing (Apache Airflow, Prefect) vs streaming (Apache Kafka, AWS Kinesis)
# Error handling and data validation
# Monitoring and alerting for pipeline failures
