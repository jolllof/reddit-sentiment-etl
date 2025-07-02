import os
from etl.extract import RedditExtractor
from config.config import load_reddit_config
# from transform import RedditTransformer  # Your future transform class
# from load import RedditLoader  # Your future load class
import structlog

def main():
    """
    Main ETL pipeline orchestrator for Reddit sentiment analysis.
    """


    logger = structlog.get_logger()
    logger.info("Starting Reddit Sentinment ETL pipeline")
    
    try:
        # Extract Phase
        logger.info("Starting extraction phase")
        config = load_reddit_config()

        extractor = RedditExtractor(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
            username=config.username,
            password=config.password)
        
        # Extract data from popular subreddits
        raw_data = extractor.extract_reddit_data(
            subreddit_source="popular",
            subreddit_limit=100,
            posts_per_subreddit=20,
            save_to_csv=True  # Save raw data for backup
        )
        
        logger.info(f"Extraction completed. Extracted {len(raw_data)} posts")
        
        # Transform Phase (placeholder for your future implementation)
        logger.info("Starting transformation phase")
        # transformer = RedditTransformer()
        # processed_data = transformer.transform_data(raw_data)
        
        # Load Phase (placeholder for your future implementation)
        logger.info("Starting load phase")
        # loader = RedditLoader()
        # loader.load_data(processed_data)
        
        logger.info("ETL pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")

if __name__ == "__main__":
    main()
