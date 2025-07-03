
from etl.extract import RedditExtractor
from config.config import load_reddit_config
from etl.transform import RedditTransformer
from models.sentiment import SentimentAnalyzer
from utilities import save_posts_to_csv
import os
# from load import RedditLoader  # Your future load class
import structlog
os.system('clear')


def main():
    """
    Main ETL pipeline orchestrator for Reddit sentiment analysis.
    """
    logger = structlog.get_logger()
    logger = logger.bind(module="main")
    subbredit_source = "popular"
    subreddit_limit=1
    posts_per_subreddit=20

    logger.info(f"*** {subbredit_source.upper()} Reddit Sentinment ETL pipeline ***")
    print('\n')

    try:
        # Extract Phase
        logger.info("EXTRACTION PHASE")
        config = load_reddit_config()

        extractor = RedditExtractor(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
            username=config.username,
            password=config.password)
        
            # Extract data from popular subreddits
        raw_data = extractor.extract_reddit_data(
            subreddit_source=subbredit_source,
            subreddit_limit=subreddit_limit,
            posts_per_subreddit=posts_per_subreddit,
            save_to_csv=False  # Save raw data for backup
        )
        logger.info(f"Extraction completed. Extracted {len(raw_data)} posts")
        print('\n')
        
        # Transform Phase (placeholder for your future implementation)
        logger.info("TRANSFORMATION PHASE")
        transformer = RedditTransformer()
        transformed_data = transformer.transform_data(
            raw_data, 
            save_to_csv=False
        )
        
        print('\n')
        logger.info("SENTIMENT ANALYSIS PHASE")
        analyzer = SentimentAnalyzer()

        analyized_data=analyzer.apply_analysis(
            transformed_data,
            save_to_csv=True
        )
        logger.info("Sentiment analysis completed and saved to CSV")

        # Load Phase (placeholder for your future implementation)
        logger.info("LOADING PHASE")
        # loader = RedditLoader()
        # loader.load_data(processed_data)
        
        logger.info("ETL pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")

if __name__ == "__main__":
    main()
