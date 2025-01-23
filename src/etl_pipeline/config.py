import os
from dotenv import load_dotenv
import logging
from rich.logging import RichHandler
from rich.traceback import install

# API KEYS
load_dotenv()
CG_API_KEY = os.getenv('CG_API_KEY')
ETH_API_KEY = os.getenv('ETH_API_KEY')

# LOGGING
install()
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'rich': {
            'format': '%(message)s',
        },
        'detailed': {
            'format': '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/etl_pipeline.log',
            'formatter': 'detailed',
            'level': 'INFO',
        },
        'console': {
            'class': 'rich.logging.RichHandler',
            'formatter': 'rich',
            'level': 'INFO',
            'rich_tracebacks': True,
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console'],
    },
}
def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

# DeFI PROTOCOLS
KEY_PROTOCOLS = [
    "uniswap",                  # DEX
    "curve-dao-token",          # DEX
    "balancer",                 # DEX
    "aave",                     # Lending
    "maker",                    # Lending
    "yearn-finance",            # Yield Farming
    "harvest-finance",          # Yield Farming
    "dai",                      # Stablecoin
    "usd-coin",                 # Stablecoin
    "tether",                   # Stablecoin
    "nftfi",                    # NFT-Fi (optionnel)
]