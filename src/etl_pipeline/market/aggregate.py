from datetime import datetime, timedelta
import pytz
from tqdm import tqdm


def aggregate_transactions(db, protocol_name, start_date, end_date):
    """
    Aggregates transaction data from the 'transactions' collection for a specified protocol
    between the given start and end dates. The aggregation computes metrics for hourly and
    daily periods.

    :param db: The MongoDB database object where the transactions collection resides.
    :param protocol_name: The name of the protocol for which the transactions are aggregated.
    :param start_date: The start date (datetime object) for filtering transactions.
    :param end_date: The end date (datetime object) for filtering transactions.
    :return: A list of aggregated transaction data for hourly and daily periods.
    """
    match_stage = {
        "$match": {
            "metadata.protocol_name": protocol_name,
            "timestamp": {"$gte": start_date, "$lt": end_date}
        }
    }
    group_stage = {
        "$group": {
            "_id": {
                "year": {"$year": "$timestamp"},
                "month": {"$month": "$timestamp"},
                "day": {"$dayOfMonth": "$timestamp"},
                "hour": {"$hour": "$timestamp"}
            },
            "original_timestamp": {"$first": "$timestamp"},
            "total_transactions": {"$sum": 1},
            "unique_users": {"$addToSet": "$from"},
            "unique_senders": {"$addToSet": "$from"},
            "unique_receivers": {"$addToSet": "$to"},
            "total_volume_eth": {"$sum": "$value (ETH)"},
            "total_gas_used": {"$sum": "$gas_used"}
        }
    }
    projection_stage = {
        "$project": {
            "total_transactions": 1,
            "unique_users": {"$size": "$unique_users"},
            "unique_senders": {"$size": "$unique_senders"},
            "unique_receivers": {"$size": "$unique_receivers"},
            "total_volume_eth": 1,
            "total_gas_used": 1,
            "original_timestamp": 1
        }
    }
    pipeline = [match_stage, group_stage, projection_stage]
    return list(db.transactions.aggregate(pipeline))


def aggregate_24h_data(db, protocol_name, hourly_data_list):
    """
    Aggregates sliding 24-hour data based on the hourly transaction data.

    :param db: The MongoDB database object where the transactions collection resides.
    :param protocol_name: The name of the protocol for which the data is aggregated.
    :param hourly_data_list: A list of hourly aggregated transaction data.
    :return: A list of enhanced data with additional 24-hour aggregated metrics.
    """
    enhanced_data = []
    for i, hourly_data in tqdm(enumerate(hourly_data_list), desc=f"Aggregating 24h data for {protocol_name}",
                               unit="hour", total=len(hourly_data_list)):
        timestamp_dict = hourly_data["_id"]
        timestamp = datetime(
            timestamp_dict["year"],
            timestamp_dict["month"],
            timestamp_dict["day"],
            timestamp_dict["hour"]
        ).replace(tzinfo=pytz.utc)
        timestamp = timestamp.replace(minute=0, second=0, microsecond=0)

        window_start_time = timestamp - timedelta(hours=23)
        match_stage_24h = {
            "$match": {
                "metadata.protocol_name": protocol_name,
                "timestamp": {"$gte": window_start_time, "$lt": timestamp}
            }
        }
        group_stage_24h = {
            "$group": {
                "_id": None,
                "total_transactions_24h": {"$sum": 1},
                "unique_users_24h": {"$addToSet": "$from"},
                "unique_senders_24h": {"$addToSet": "$from"},
                "unique_receivers_24h": {"$addToSet": "$to"},
                "total_volume_eth_24h": {"$sum": "$value (ETH)"},
                "total_gas_used_24h": {"$sum": "$gas_used"}
            }
        }
        projection_stage_24h = {
            "$project": {
                "total_transactions_24h": 1,
                "unique_users_24h": {"$size": "$unique_users_24h"},
                "unique_senders_24h": {"$size": "$unique_senders_24h"},
                "unique_receivers_24h": {"$size": "$unique_receivers_24h"},
                "total_volume_eth_24h": 1,
                "total_gas_used_24h": 1,
            }
        }
        pipeline_24h = [match_stage_24h, group_stage_24h, projection_stage_24h]
        sliding_24h_result = list(db.transactions.aggregate(pipeline_24h))

        if sliding_24h_result:
            sliding_data = sliding_24h_result[0]
            enhanced_data.append({**hourly_data, **sliding_data})
        else:
            enhanced_data.append(hourly_data)
    return enhanced_data


