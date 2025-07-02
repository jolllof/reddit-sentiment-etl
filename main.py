from etl.extract import *
from etl.transform import *
import argparse
import os
from datetime import datetime, timedelta
import praw
import pandas as pd
from utilities import *
import structlog

logger = structlog.get_logger()
logger=logger.bind(module="main")
os.system('clear')
current_datetime = datetime.now()


def main():
    logger.info("Getting popular subreddits from Reddit")
    popular_subreddits = get_popular_subreddits(reddit, 100)

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


if __name__ == "__main__":
    main()


