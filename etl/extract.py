import argparse
import os
from datetime import datetime, timedelta
from requests_oauthlib import OAuth1

from utilities import *
os.system('clear')

import structlog
logger = structlog.get_logger()

consumer_key='a2A6kLFlbDNJMiuI3Sl1BDxLE'
consumer_secret='bWP0qEmf7xSygdVrMXVKHadrHcTpCRgTVabn9RUzXwCfxPObfK'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMat2gEAAAAAbSXpy%2FQ8lFwAwlYH6%2BDXgA9R5dc%3DvhRoAfdvyUhhbETcVPaDhvMk3NsqrP9EBjHukbjZYUYbHfwThY'
access_token='1936517666514104320-vBYJwuRZFLDKumokPNARX3wPv5te3s'
access_token_secret='3I6YzB5eQPocJPX48BloZBtB0ia8yseOlkKTSMti1xkG3'

def main(args):
    logger.info("Initiating Data Extract")
    base_url = 'https://api.twitter.com/2'
    users = '/users/me'
    following = '/users/:id/following'
    
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    
    # Get user data
    logger.info("Fetching user data")
    url = f"{base_url}{users}"
    logger.info(f"URL: {url}")
    res = get_data(url, auth)
    user_id = res.json().get('data', {}).get('id', None)
    name= res.json().get('data', {}).get('name', None)
    username= res.json().get('data', {}).get('username', None)

    # Get following data

    # logger.info("Fetching following data")
    # url = f"{base_url}{following.replace(':id', user_id)}"
    # params = {
    #     "max_results": 1000,
    #     "user.fields": "id,name,username,verified",
    # }
    # logger.info(f"URL: {url}")

    # res = get_data(url, auth)
    # logger.info(f"Response: {res}")

    
    

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


