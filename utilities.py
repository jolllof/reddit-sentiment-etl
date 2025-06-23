import requests
import structlog
logger = structlog.get_logger()

def get_data(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error Fetching {url} \n {response}")
        return []
    else:
        return response
        logger.info(f"Utilities: Successfully fetched data from {url}")