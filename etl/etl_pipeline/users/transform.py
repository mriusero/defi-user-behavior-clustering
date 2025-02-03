import json
from collections import defaultdict


def default_user_data() -> dict:
    """
    Returns a dictionary with default user data.
    """
    return {
        "address": None,
        "sent_count": 0,
        "received_count": 0,
        "total_sent (ETH)": 0.0,
        "total_received (ETH)": 0.0,
        "first_seen": None,
        "last_seen": None,
        "protocols_used": defaultdict(default_protocol_data),
        "protocol_types": defaultdict(int),
        "transactions": [],
    }


def default_protocol_data() -> dict:
    """
    Returns a dictionary with default protocol data.
    """
    return {
        "count": 0,
        "blockchain": None,
        "contract_id": None,
    }


def transform_to_user_data(transactions: list) -> defaultdict:
    """
    Transforms a batch of transactions into user data with transaction details.
    """
    users_data = defaultdict(default_user_data)

    for tx in transactions:
        if isinstance(tx, str):
            tx = json.loads(tx)

        from_address = tx["from"]
        to_address = tx["to"]
        value_eth = tx["value (ETH)"]
        timestamp = tx["timestamp"]
        gas_used = tx["gas_used"]  # Extract gas used
        protocol_name = tx.get("metadata", {}).get("protocol_name", None)
        protocol_type = tx.get("metadata", {}).get("type", None)
        protocol_blockchain = tx.get("metadata", {}).get("blockchain", None)
        protocol_contract_id = tx.get("metadata", {}).get("contract_id", None)

        def update_user(address, is_sender):
            user = users_data[address]
            if user["address"] is None:
                user["address"] = address
            user["last_seen"] = (
                max(user["last_seen"], timestamp) if user["last_seen"] else timestamp
            )
            user["first_seen"] = (
                min(user["first_seen"], timestamp) if user["first_seen"] else timestamp
            )
            if is_sender:
                user["sent_count"] += 1
                user["total_sent (ETH)"] += value_eth
            else:
                user["received_count"] += 1
                user["total_received (ETH)"] += value_eth
            if protocol_name:
                protocols = user["protocols_used"][protocol_name]
                protocols["count"] += 1
                protocols["blockchain"] = protocol_blockchain
                protocols["contract_id"] = protocol_contract_id
            if protocol_type:
                user["protocol_types"][protocol_type] += 1

            user["transactions"].append(
                {
                    "transaction_hash": tx["transaction_hash"],
                    "timestamp": timestamp,
                    "value (ETH)": value_eth,
                    "is_sender": is_sender,
                    "gas_used": gas_used,
                    "protocol_name": protocol_name,
                    "protocol_type": protocol_type,
                    "blockchain": protocol_blockchain,
                    "contract_id": protocol_contract_id,
                }
            )

        update_user(from_address, is_sender=True)
        update_user(to_address, is_sender=False)

    return users_data
