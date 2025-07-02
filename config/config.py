import os
from dataclasses import dataclass

@dataclass
class RedditConfig:
    """Configuration class for Reddit API credentials"""
    client_id: str
    client_secret: str
    user_agent: str
    username: str
    password: str

def load_reddit_config() -> RedditConfig:
    """
    Load Reddit configuration from environment variables.
    Falls back to default values if environment variables are not set.
    """
    return RedditConfig(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD')
    )
