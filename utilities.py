import requests
import structlog

logger = structlog.get_logger()
logger = logger.bind(module="utilities")


def save_posts_to_csv(df, current_datetime, filename=None):
    """
    Save posts DataFrame to CSV file.

    Args:
        df(pandas.DataFrame): DataFrame containing post data
        filename (str): Optional custom filename

    Returns:
        str: Path to saved file
    """
    if filename is None:
        filename = f"data/hot_posts_{current_datetime.strftime('%Y%m%d_%H%M%S')}.csv"
    else:
        filename = f"data/{filename}_hot_posts_{current_datetime.strftime('%Y%m%d_%H%M%S')}.csv"

    df.to_csv(filename, index=False)
    logger.info(f"Saved {len(df)} posts to {filename}")
    return filename
