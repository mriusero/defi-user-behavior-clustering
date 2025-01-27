import logging.config
import multiprocessing

from etl_pipeline import process_etl_pipeline
from etl_pipeline.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
multiprocessing.log_to_stderr(logging.DEBUG)

def run_etl():

    process_etl_pipeline(
        protocols=False,
        contracts=False,
        transactions=False,
        users=False,
        price=False,
        market=False,
        dataset=False,
        save=False,
    )

if __name__ == '__main__':
    run_etl()