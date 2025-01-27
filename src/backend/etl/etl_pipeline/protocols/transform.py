import hashlib


def generate_protocol_id(name):
    """
    Generate a unique protocol_id based on the protocol name.
    :param:
        name (str): The name of the protocol.
    :return:
        str: A unique protocol_id.
    """
    normalized_name = (
        name.strip().lower()
    )  # Normalize the name (lowercase and strip whitespace)
    protocol_id = hashlib.md5(
        normalized_name.encode()
    ).hexdigest()  # Generate a hash from the normalized name

    return protocol_id


def infer_protocol_type(protocol_id):
    """
    Infers the type of a protocol based on its identifier.
    :param:
        protocol_id (str): The identifier of the protocol.
    :return:
        str: The inferred type of the protocol (e.g., DEX, Lending, Yield Farming, Stablecoin, NFT-Fi, or DeFi).
    """
    if protocol_id in ["uniswap", "sushiswap", "curve-dao-token", "balancer"]:
        return "DEX"
    elif protocol_id in ["aave", "compound", "maker"]:
        return "Lending"
    elif protocol_id in ["yearn-finance", "harvest-finance", "curve-dao-token"]:
        return "Yield Farming"
    elif protocol_id in ["dai", "usd-coin", "tether"]:
        return "Stablecoin"
    elif protocol_id in ["nftfi", "nifty-gateway", "opensea"]:
        return "NFT-Fi"
    else:
        return "DeFi"
