import requests
import structlog
logger = structlog.get_logger()


def get_data(url, auth):
    response = requests.get(url, auth=auth)
    logger.info(response)

    if response.status_code != 200:
        print(f"Error Fetching {url} \n {response}")
        print(response.text)
        return []
    else:
        return response
        logger.info(f"Utilities: Successfully fetched data from {url}")


def post_data(url, auth, params):
    response = requests.post(url, auth=auth, params=params)

    if response.status_code != 200:
        print(f"Error Fetching {url} \n {response}")
        return []
    else:
        return response.text
        logger.info(f"Utilities: Successfully fetched data from {url}")