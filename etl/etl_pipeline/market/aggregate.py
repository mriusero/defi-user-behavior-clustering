import pandas as pd
from tqdm import tqdm
from ..mongodb_handler import get_mongo_collection

def aggregate_transactions(df, time_delta=None):
    """
    Aggregates the transaction data from the MongoDB collection based on the given DataFrame.

    :param df: A DataFrame containing the timestamps and protocol names.
    :param time_delta: The time interval (in hours) used to group the transactions.
    :return: A DataFrame enriched with the aggregated transaction data.
    :raise: Exception: If an error occurs during the aggregation process.
    """
    transactions_collection = get_mongo_collection(
        db_name="defi_db", collection_name="transactions"
    )
    results = []

    for _, row in tqdm(
        df.iterrows(),
        total=len(df),
        desc=f"Aggregating transactions for {df['protocol_name'][0]} ; frequency={time_delta}h ",
        unit="row",
    ):
        start_time = pd.to_datetime(row["timestamp"])
        end_time = start_time + pd.Timedelta(hours=time_delta)
        query = {
            "metadata.protocol_name": row["protocol_name"],
            "timestamp": {"$gte": start_time, "$lt": end_time},
        }
        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": None,
                    "nb_tx": {"$sum": 1},  # Total number of transactions
                    "unique_senders": {"$addToSet": "$from"},  # Unique senders
                    "unique_receivers": {"$addToSet": "$to"},  # Unique receivers
                    "total_value_eth": {
                        "$sum": "$value (ETH)"
                    },  # Total value of transactions in ETH
                    "avg_value_eth_per_tx": {
                        "$avg": "$value (ETH)"
                    },  # Average value per transaction
                    "max_value_eth": {
                        "$max": "$value (ETH)"
                    },  # Maximum transaction value in ETH
                    "min_value_eth": {
                        "$min": "$value (ETH)"
                    },  # Minimum transaction value in ETH
                    "std_value_eth": {
                        "$stdDevPop": "$value (ETH)"
                    },  # Standard deviation of transaction values
                    "total_gas_used": {
                        "$sum": "$gas_used"
                    },  # Total gas used in transactions
                    "avg_gas_used": {"$avg": "$gas_used"},  # Average gas used
                    "max_gas_used": {
                        "$max": "$gas_used"
                    },  # Maximum gas used in a transaction
                    "min_gas_used": {
                        "$min": "$gas_used"
                    },  # Minimum gas used in a transaction
                    "std_gas_used": {
                        "$stdDevPop": "$gas_used"
                    },  # Standard deviation of gas used
                    "num_errors": {
                        "$sum": {"$cond": [{"$eq": ["$is_error", "1"]}, 1, 0]}
                    },  # Count of transactions with errors
                    "error_rate": {
                        "$avg": {"$cond": [{"$eq": ["$is_error", "1"]}, 1, 0]}
                    },  # Error rate
                    "median_value_eth": {
                        "$avg": {
                            "$cond": [
                                {"$eq": [{"$mod": ["$value (ETH)", 2]}, 0]},
                                "$value (ETH)",
                                None,
                            ]
                        }
                    },  # Median value in ETH
                }
            },
            {
                "$project": {
                    "nb_tx": 1,
                    "unique_senders": 1,
                    "unique_receivers": 1,
                    "total_value_eth": 1,
                    "avg_value_eth_per_tx": 1,
                    "max_value_eth": 1,
                    "min_value_eth": 1,
                    "std_value_eth": 1,
                    "total_gas_used": 1,
                    "avg_gas_used": 1,
                    "max_gas_used": 1,
                    "min_gas_used": 1,
                    "std_gas_used": 1,
                    "num_errors": 1,
                    "error_rate": 1,
                    "median_value_eth": 1,
                }
            },
        ]

        aggregation_result = list(transactions_collection.aggregate(pipeline))

        if aggregation_result:
            agg_data = aggregation_result[0]
            results.append(
                {
                    "timestamp": row["timestamp"],
                    "protocol_name": row["protocol_name"],
                    "nb_tx": agg_data.get("nb_tx", 0),
                    "nb_unique_senders": len(agg_data.get("unique_senders", [])),
                    "nb_unique_receivers": len(agg_data.get("unique_receivers", [])),
                    "total_value_eth": agg_data.get("total_value_eth", 0.0),
                    "avg_value_eth_per_tx": agg_data.get("avg_value_eth_per_tx", 0.0),
                    "max_value_eth": agg_data.get(
                        "max_value_eth", 0.0
                    ),  # Maximum value in ETH
                    "min_value_eth": agg_data.get(
                        "min_value_eth", 0.0
                    ),  # Minimum value in ETH
                    "std_value_eth": agg_data.get(
                        "std_value_eth", 0.0
                    ),  # Standard deviation in ETH
                    "total_gas_used": agg_data.get("total_gas_used", 0.0),
                    "avg_gas_used": agg_data.get("avg_gas_used", 0.0),
                    "max_gas_used": agg_data.get("max_gas_used", 0.0),
                    "min_gas_used": agg_data.get("min_gas_used", 0.0),
                    "std_gas_used": agg_data.get("std_gas_used", 0.0),
                    "num_errors": agg_data.get("num_errors", 0),
                    "error_rate": agg_data.get("error_rate", 0.0),
                    "median_value_eth": agg_data.get(
                        "median_value_eth", 0.0
                    ),  # Median value in ETH
                }
            )
        else:
            results.append(
                {
                    "timestamp": row["timestamp"],
                    "protocol_name": row["protocol_name"],
                    "nb_tx": 0,
                    "nb_unique_senders": 0,
                    "nb_unique_receivers": 0,
                    "total_value_eth": 0.0,
                    "avg_value_eth_per_tx": 0.0,
                    "max_value_eth": 0.0,
                    "min_value_eth": 0.0,
                    "std_value_eth": 0.0,
                    "total_gas_used": 0.0,
                    "avg_gas_used": 0.0,
                    "max_gas_used": 0.0,
                    "min_gas_used": 0.0,
                    "std_gas_used": 0.0,
                    "num_errors": 0,
                    "error_rate": 0.0,
                    "median_value_eth": 0.0,
                }
            )

        agg_df = pd.DataFrame(results)

    if time_delta:
        suffix = f"_{time_delta}h"
        agg_df = agg_df.rename(
            columns=lambda x: (
                f"{x}{suffix}" if x not in ["protocol_name", "timestamp"] else x
            )
        )

    enriched_df = df.merge(agg_df, on=["timestamp", "protocol_name"], how="left")

    return enriched_df
