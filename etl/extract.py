import argparse
import os
from datetime import datetime, timedelta
import praw
import pandas as pd
from utilities import *

import structlog
logger = structlog.get_logger()
logger=logger.bind(module="extract")
current_datetime = datetime.now()


reddit = praw.Reddit(
    client_id="SLxpSSHPC6W8_G7E_jnwHQ",
    client_secret="YkCYpwFnMJINtKH3w3ltytFkuRwKnQ",
    user_agent="sentiment_analysis",
    username="jolllof  ",
    password="Jarvis2.0"
)


def get_popular_subreddits(reddit_instance, limit=None):
    """
    Fetches the top subreddits from Reddit.
    :param reddit_instance: An instance of the Reddit API client.
    :param limit: The number of subreddits to fetch.
    :return: A list of subreddit names.
    """
    subreddits = []
    for subreddit in reddit_instance.subreddits.popular(limit=limit):
        subreddits.append(subreddit)
    return subreddits

def get_user_subreddits(reddit_instance, limit=None):
    """
    Fetches the subreddits that the authenticated user is subscribed to.
    :param reddit_instance: An instance of the Reddit API client.
    :param limit: The number of subreddits to fetch.
    :return: A list of subreddit names.
    """
    subreddits = []
    for subreddit in reddit_instance.user.subreddits(limit=limit):
        subreddits.append(subreddit.display_name)
    return subreddits

def get_hot_posts_from_subreddits(subreddits, reddit, limit=20):

    """
    Fetches the top posts from multiple subreddits.
    :param subreddit_names: A list of subreddit names.
    :param reddit_instance: An instance of the Reddit API client.
    :param limit: The number of posts to fetch from each subreddit.
    :return: A dictionary with subreddit names as keys and lists of post titles and scores as values.
    """
    posts=[]
    for sub in subreddits:
        logger.info(f"Fetching hot posts from: {sub}")

        subreddit = reddit.subreddit(sub)
        for post in subreddit.hot(limit=10):
            posts.append(
                {
                    "subreddit": sub,
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "author": post.author.name if post.author else "deleted",
                    "created_utc": datetime.utcfromtimestamp(post.created_utc),
                }
            )

    posts_df = pd.DataFrame(posts)
    posts_df.to_csv(f"data/hot_posts_{current_datetime}.csv", index=False)
