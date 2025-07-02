import argparse
import os
from datetime import datetime, timedelta
import praw
import pandas as pd
from utilities import *


import structlog
logger = structlog.get_logger()
os.system('clear')
current_datetime = datetime.now()

client_id="SLxpSSHPC6W8_G7E_jnwHQ",
client_secret="YkCYpwFnMJINtKH3w3ltytFkuRwKnQ",
user_agent="sentiment_analysis",
username="jolllof  ",
password="Jarvis2.0"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
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
        logger.info(f"Fetching hot posts from subreddit: {sub}")

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
    posts_df.to_csv(f"hot_posts{current_datetime}.csv", index=False)

def main(args):
    logger.info("Getting popular subreddits from Reddit")
    popular_subreddits = get_popular_subreddits(reddit, 10)

    #user_subreddits = get_user_subreddits(reddit)
    nsfw = []
    clean = []
    logger.info("Removing NSFW subreddits")
    for subreddit in popular_subreddits:
        if subreddit.over18: 
            nsfw.append(subreddit.display_name)
        else:
            clean.append(subreddit.display_name)

    logger.info(f"Found {len(popular_subreddits)} popular subreddits, {len(nsfw)} NSFW and {len(clean)} clean subreddits")
    logger.info("Getting top posts from clean subreddits") 
    get_hot_posts_from_subreddits(clean, reddit)


    
    
    # subreddit = reddit.subreddit("python")
    # for post in subreddit.hot(limit=10):
    #     print(f"{post.title} (Score: {post.score})")

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--set",
        metavar="KEY=VALUE",
        nargs="+",
        help="""
			Arguments need to be passed in the form of --set key1=val1 key2=val2 etc...
			Example Arguments:
			Python3 -m prime --set args_group="robinhood"
		""",
    )
    args = parser.parse_args()
    if args.set:
        args = {v.split("=", 1)[0]: v.split("=", 1)[1] for v in list(args.set)}

    main(args)


