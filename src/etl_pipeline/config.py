from dotenv import load_dotenv
import os

load_dotenv()
CG_API_KEY = os.getenv('CG_API_KEY')
ETH_API_KEY = os.getenv('ETH_API_KEY')


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/etl_pipeline.log',
            'formatter': 'default',
            'level': 'DEBUG'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level':'INFO',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console'],
    },
}


KEY_PROTOCOLS = [                               # Liste des protocoles clés et leurs identifiants sur CoinGecko
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