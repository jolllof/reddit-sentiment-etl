
import argparse
import os
from datetime import datetime, timedelta
import praw
import pandas as pd
from utilities import save_posts_to_csv

import structlog

class RedditExtractor:
    """
    A class to handle Reddit data extraction for sentiment analysis ETL pipeline.
    """
    
    def __init__(self, client_id=None, client_secret=None, user_agent=None, username=None, password=None):
        """
        Initialize the RedditExtractor with Reddit API credentials.
        
        Args:
            client_id (str): Reddit API client ID
            client_secret (str): Reddit API client secret
            user_agent (str): User agent string for API requests
            username (str): Reddit username
            password (str): Reddit password
        """
        self.logger = structlog.get_logger()
        self.logger = self.logger.bind(module="extract")
        self.current_datetime = datetime.now()
        
        # Initialize Reddit instance
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def get_popular_subreddits(self, limit=None):
        """
        Fetches the top subreddits from Reddit.
        
        Args:
            limit (int): The number of subreddits to fetch.
            
        Returns:
            list: A list of subreddit objects.
        """
        self.logger.info(f"Fetching popular subreddits with limit: {limit}")
        subreddits = []
        try:
            for subreddit in self.reddit.subreddits.popular(limit=limit):
                subreddits.append(subreddit)
            self.logger.info(f"Successfully fetched {len(subreddits)} popular subreddits")
        except Exception as e:
            self.logger.error(f"Error fetching popular subreddits: {e}")
            raise
        
        return subreddits
    
    def get_user_subreddits(self, limit=None):
        """
        Fetches the subreddits that the authenticated user is subscribed to.
        
        Args:
            limit (int): The number of subreddits to fetch.
            
        Returns:
            list: A list of subreddit names.
        """
        self.logger.info(f"Fetching user subreddits with limit: {limit}")
        subreddits = []
        try:
            for subreddit in self.reddit.user.subreddits(limit=limit):
                subreddits.append(subreddit.display_name)
            self.logger.info(f"Successfully fetched {len(subreddits)} user subreddits")
        except Exception as e:
            self.logger.error(f"Error fetching user subreddits: {e}")
            raise
        
        return subreddits
    
    def get_hot_posts_from_subreddits(self, subreddits, limit=10):
        """
        Fetches the hot posts from multiple subreddits.
        
        Args:
            subreddits (list): A list of subreddit names.
            limit (int): The number of posts to fetch from each subreddit.
            
        Returns:
            pandas.DataFrame: DataFrame containing post data.
        """
        self.logger.info(f"Fetching hot posts from {len(subreddits)} subreddits")
        posts = []
        
        for sub in subreddits:
            try:
                self.logger.info(f"Fetching hot posts from: {sub}")
                subreddit = self.reddit.subreddit(sub)
                
                for post in subreddit.hot(limit=limit):
                    posts.append({
                        "subreddit": sub,
                        "title": post.title,
                        "score": post.score,
                        "url": post.url,
                        "author": post.author.name if post.author else "deleted",
                        "created_utc": datetime.utcfromtimestamp(post.created_utc),
                        "extracted_at": self.current_datetime
                    })
            except Exception as e:
                self.logger.error(f"Error fetching posts from {sub}: {e}")
                continue
        
        posts_df = pd.DataFrame(posts)
        self.logger.info(f"Successfully extracted {len(posts_df)} posts")
        return posts_df
    
    def extract_reddit_data(self, subreddit_source="popular", subreddit_limit=10, posts_per_subreddit=10, save_to_csv=True):
        """
        Main extraction method that orchestrates the entire extraction process.
        
        Args:
            subreddit_source (str): "popular" or "user" - source of subreddits
            subreddit_limit (int): Number of subreddits to fetch
            posts_per_subreddit (int): Number of posts to fetch per subreddit
            save_to_csv (bool): Whether to save results to CSV
            
        Returns:
            pandas.DataFrame: DataFrame containing extracted post data
        """
        self.logger.info("Starting Reddit data extraction")
        
        # Get subreddits
        if subreddit_source == "popular":
            subreddit_objects = self.get_popular_subreddits(limit=subreddit_limit)
            subreddit_names = [sub.display_name for sub in subreddit_objects]
        elif subreddit_source == "user":
            subreddit_names = self.get_user_subreddits(limit=subreddit_limit)
        else:
            raise ValueError("subreddit_source must be 'popular' or 'user'")
        
        # Get posts
        posts_df = self.get_hot_posts_from_subreddits(subreddit_names, limit=posts_per_subreddit)
        
        # Save to CSV if requested
        if save_to_csv:
            filename=save_posts_to_csv(posts_df, current_datetime=self.current_datetime, filename="extracted")
        
        self.logger.info("Reddit data extraction completed successfully")
        return posts_df


# For backward compatibility and standalone execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Reddit data for sentiment analysis")
    parser.add_argument("--subreddit-source", choices=["popular", "user"], default="popular",
                        help="Source of subreddits to extract from")
    parser.add_argument("--subreddit-limit", type=int, default=10,
                        help="Number of subreddits to fetch")
    parser.add_argument("--posts-per-subreddit", type=int, default=10,
                        help="Number of posts to fetch per subreddit")
    
    args = parser.parse_args()
    
    # Create extractor and run extraction
    extractor = RedditExtractor()
    extractor.extract_reddit_data(
        subreddit_source=args.subreddit_source,
        subreddit_limit=args.subreddit_limit,
        posts_per_subreddit=args.posts_per_subreddit
    )
    