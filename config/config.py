import os
from dataclasses import dataclass
import yaml

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

def load_db_config() -> dict:
    """
    Load database configuration from environment variables.
    Falls back to default values if environment variables are not set.
    """
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'reddit_etl'),
        'user': os.getenv('DB_USER', 'reddit_etl'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'port': int(os.getenv('DB_PORT', 5432))
    }

def load_yaml_config(values: str) -> dict:
    """
    Load configuration from a YAML file.
    This function can be expanded to read from a specific YAML file if needed.
    """
    config_path = "config/config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        return config.get(values, {})
    