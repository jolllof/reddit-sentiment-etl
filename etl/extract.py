import argparse
import os
from datetime import datetime, timedelta

from utilities import *

import structlog
logger = structlog.get_logger()

def main(args):
    logger.info("Initiating Data Extract")
    


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