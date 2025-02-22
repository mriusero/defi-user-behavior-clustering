import numpy as np

def performances_scores(features):
    """ Calculate various scores based on the features of Ethereum addresses. """

    # ROI
    """
    Calcule le retour sur investissement (ROI) basé sur le flux net d'ETH.
    - Valeur forte : Indique un haut rendement ou profit.
    - Valeur faible : Indique un faible rendement ou perte.

    Le flux net d'ETH (net_flow_eth) est la différence entre les ETH reçus et envoyés.
    Une valeur positive (forte) indique un profit, ce qui est souhaitable.
    Une valeur négative (faible) indique une perte, ce qui n'est pas souhaitable.
    """
    features['roi'] = features['net_flow_eth']

    # Activity Score
    """
    Évalue le score d'activité basé sur les transactions reçues et envoyées.
    - Valeur forte : Indique une activité élevée et une participation active.
    - Valeur faible : Indique une faible activité ou inactivité.

    Les variables utilisées sont :
    - received_count : Nombre de transactions reçues.
    - total_received_eth : Total d'ETH reçus.
    - sent_count : Nombre de transactions envoyées.
    - total_sent_eth : Total d'ETH envoyés.

    Une valeur forte est souhaitable car elle indique une activité élevée.
    """
    features['activity_score'] = (features['received_count'] +
                                  features['total_received_eth'] +
                                  features['sent_count'] +
                                  features['total_sent_eth'])

    # Interaction Diversity
    """
    Mesure la diversité des interactions basée sur différents types de transactions.
    - Valeur forte : Indique une grande diversité dans les types d'interactions.
    - Valeur faible : Indique une faible diversité ou une concentration sur certains types d'interactions.

    Les variables utilisées sont :
    - type_dex : Transactions sur des plateformes d'échange décentralisées.
    - type_lending : Transactions de prêt.
    - type_stablecoin : Transactions impliquant des stablecoins.
    - type_yield_farming : Transactions de yield farming.
    - type_nft_fi : Transactions impliquant des NFT.

    Une valeur forte est souhaitable car elle indique une diversité élevée.
    """
    features['interaction_diversity'] = (features['type_dex'] +
                                         features['type_lending'] +
                                         features['type_stablecoin'] +
                                         features['type_yield_farming'] +
                                         features['type_nft_fi'])

    # Engagement Diversity
    """
    Évalue la diversité de l'engagement basée sur l'interaction avec diverses plateformes.
    - Valeur forte : Indique une participation active sur plusieurs plateformes.
    - Valeur faible : Indique une participation limitée ou concentrée sur quelques plateformes.

    Les variables utilisées sont :
    - curve_dao_count : Interactions avec Curve DAO.
    - aave_count : Interactions avec Aave.
    - tether_count : Interactions avec Tether.
    - uniswap_count : Interactions avec Uniswap.
    - maker_count : Interactions avec Maker.
    - yearn_finance_count : Interactions avec Yearn Finance.
    - usdc_count : Interactions avec USDC.
    - dai_count : Interactions avec DAI.
    - balancer_count : Interactions avec Balancer.
    - harvest_finance_count : Interactions avec Harvest Finance.
    - nftfi_count : Interactions avec NFTfi.

    Une valeur forte est souhaitable car elle indique une diversité d'engagement élevée.
    """
    features['engagement_diversity'] = (features['curve_dao_count'] +
                                        features['aave_count'] +
                                        features['tether_count'] +
                                        features['uniswap_count'] +
                                        features['maker_count'] +
                                        features['yearn_finance_count'] +
                                        features['usdc_count'] +
                                        features['dai_count'] +
                                        features['balancer_count'] +
                                        features['harvest_finance_count'] +
                                        features['nftfi_count'])

    # Sending Behavior
    """
    Analyse le comportement d'envoi basé sur les statistiques d'ETH envoyé.
    - Valeur forte : Indique un comportement d'envoi actif et varié.
    - Valeur faible : Indique un comportement d'envoi inactif ou uniforme.

    Les variables utilisées sont :
    - max_sent_eth : Maximum d'ETH envoyé dans une transaction.
    - min_sent_eth : Minimum d'ETH envoyé dans une transaction.
    - avg_sent_eth : Moyenne d'ETH envoyé par transaction.
    - med_sent_eth : Médiane d'ETH envoyé par transaction.
    - std_sent_eth : Écart-type d'ETH envoyé par transaction.

    Une valeur forte est souhaitable car elle indique un comportement d'envoi actif.
    """
    features['sending_behavior'] = (features['max_sent_eth'] * 2 +
                                    features['min_sent_eth'] * -1 +
                                    features['avg_sent_eth'] * 0.5 +
                                    features['med_sent_eth'] * 0.5 +
                                    features['std_sent_eth'] * 0.5)


    # Sending Fee Efficiency
    """
    Évalue l'efficacité des frais d'envoi basée sur les coûts de gaz.
    - Valeur forte : Indique une utilisation efficace et optimisée des frais de gaz.
    - Valeur faible : Indique une utilisation inefficace ou excessive des frais de gaz.

    Les variables utilisées sont :
    - avg_gas_efficiency_sent : Efficacité moyenne des frais de gaz pour les transactions envoyées.
    - max_sent_gas : Maximum de gaz utilisé pour une transaction envoyée.
    - min_sent_gas : Minimum de gaz utilisé pour une transaction envoyée.

    Une valeur forte est souhaitable car elle indique une utilisation efficace des frais de gaz.
    """
    denominator = features['max_sent_gas'] + features['min_sent_gas']
    sending_fee_efficiency = np.where(denominator != 0,
                                      features['avg_gas_efficiency_sent'] / denominator,
                                      0)
    features['sending_fee_efficiency'] = sending_fee_efficiency

    # Receiving Behavior
    """
    Analyse le comportement de réception basé sur les statistiques d'ETH reçu.
    - Valeur forte : Indique un comportement de réception actif et varié.
    - Valeur faible : Indique un comportement de réception inactif ou uniforme.

    Les variables utilisées sont :
    - max_received_eth : Maximum d'ETH reçu dans une transaction.
    - min_received_eth : Minimum d'ETH reçu dans une transaction.
    - avg_received_eth : Moyenne d'ETH reçu par transaction.
    - med_received_eth : Médiane d'ETH reçu par transaction.
    - std_received_eth : Écart-type d'ETH reçu par transaction.

    Une valeur forte est souhaitable car elle indique un comportement de réception actif.
    """
    features['receiving_behavior'] = (features['max_received_eth'] * 2 +
                                      features['min_received_eth'] * -1 +
                                      features['avg_received_eth'] * 0.5 +
                                      features['med_received_eth'] * 0.5 +
                                      features['std_received_eth'] * 0.5)

    # Receiving Fee Efficiency
    """
    Évalue l'efficacité des frais de réception basée sur les coûts de gaz.
    - Valeur forte : Indique une utilisation efficace et optimisée des frais de gaz.
    - Valeur faible : Indique une utilisation inefficace ou excessive des frais de gaz.

    Les variables utilisées sont :
    - avg_gas_efficiency_received : Efficacité moyenne des frais de gaz pour les transactions reçues.
    - max_received_gas : Maximum de gaz utilisé pour une transaction reçue.
    - min_received_gas : Minimum de gaz utilisé pour une transaction reçue.

    Une valeur forte est souhaitable car elle indique une utilisation efficace des frais de gaz.
    """
    denominator = features['max_received_gas'] + features['min_received_gas']
    receiving_fee_efficiency = np.where(denominator != 0,
                                        features['avg_gas_efficiency_received'] / denominator,
                                        0)

    features['receiving_fee_efficiency'] = receiving_fee_efficiency

    # Global Fee Efficiency
    """
    Évalue l'efficacité globale des frais basée sur les coûts de gaz pour les envois et réceptions.
    - Valeur forte : Indique une utilisation globale efficace des frais de gaz.
    - Valeur faible : Indique une utilisation globale inefficace des frais de gaz.

    Les variables utilisées sont :
    - avg_gas_efficiency_sent : Efficacité moyenne des frais de gaz pour les transactions envoyées.
    - avg_gas_efficiency_received : Efficacité moyenne des frais de gaz pour les transactions reçues.

    Une valeur forte est souhaitable car elle indique une utilisation globale efficace des frais de gaz.
    """
    features['global_fee_efficiency'] = (features['avg_gas_efficiency_sent'] +
                                         features['avg_gas_efficiency_received'])


    # Frequency Efficiency
    """
    Mesure l'efficacité de la fréquence des transactions.
    - Valeur forte : Indique une fréquence de transaction optimale.
    - Valeur faible : Indique une fréquence de transaction inefficace ou irrégulière.

    Les variables utilisées sont :
    - tx_frequency_sent : Fréquence des transactions envoyées.
    - tx_frequency_received : Fréquence des transactions reçues.

    Une valeur forte est souhaitable car elle indique une fréquence optimale.
    """
    features['frequency_efficiency'] = (features['tx_frequency_sent'] +
                                        features['tx_frequency_received'])

    # Timing Efficiency
    """
    Évalue l'efficacité du timing des transactions basée sur les heures de pointe.
    - Valeur forte : Indique un timing optimal des transactions (en dehors des heures de pointe).
    - Valeur faible : Indique un timing inefficace ou mal synchronisé des transactions (pendant les heures de pointe).

    Les variables utilisées sont :
    - peak_hour_sent : Pourcentage de transactions envoyées pendant les heures de pointe.
    - peak_hour_received : Pourcentage de transactions reçues pendant les heures de pointe.
    - peak_count_sent : Nombre de transactions envoyées pendant les heures de pointe.
    - peak_count_received : Nombre de transactions reçues pendant les heures de pointe.

    Une valeur forte est souhaitable car elle indique un timing optimal.
    """
    features['peak_count_sent_normalized'] = features['peak_count_sent'] / features['peak_count_sent'].max()
    features['peak_count_received_normalized'] = features['peak_count_received'] / features['peak_count_received'].max()

    features['timing_efficiency'] = ((1 - features['peak_hour_sent']) +
                                 (1 - features['peak_hour_received']) +
                                 (1 - features['peak_count_sent_normalized']) +
                                 (1 - features['peak_count_received_normalized']))

    # Global Market Exposure
    """
    Calcule un score global d'exposition au marché basé sur divers facteurs.
    - Valeur forte : Indique une forte exposition et participation au marché, en maximisant les aspects positifs et minimisant les négatifs.
    - Valeur faible : Indique une faible exposition ou participation limitée au marché.

    Les variables utilisées sont :
    - total_volume_exposure : Exposition au volume total des transactions.
    - total_gas_exposure : Exposition aux coûts de gaz.
    - total_liquidity_exposure : Exposition à la liquidité.
    - total_activity_exposure : Exposition à l'activité.
    - total_user_adoption_exposure : Exposition à l'adoption par les utilisateurs.
    - total_high_value_exposure : Exposition aux transactions de haute valeur.
    - total_volatility_exposure : Exposition à la volatilité.
    - total_error_exposure : Exposition aux erreurs.
    - total_gas_volatility_exposure : Exposition à la volatilité des coûts de gaz.
    - total_error_volatility_exposure : Exposition à la volatilité des erreurs.

    Une valeur forte est souhaitable car elle indique une forte exposition au marché.
    """
    positive_exposure = (features['total_volume_exposure'] +
                         features['total_gas_exposure'] +
                         features['total_liquidity_exposure'] +
                         features['total_activity_exposure'] +
                         features['total_user_adoption_exposure'] +
                         features['total_high_value_exposure'])

    negative_exposure = ((1 - features['total_volatility_exposure']) +
                         (1 - features['total_error_exposure']) +
                         (1 - features['total_gas_volatility_exposure']) +
                         (1 - features['total_error_volatility_exposure']))
    features['global_market_exposure_score'] = positive_exposure + negative_exposure

    # Risk Index
    """
    Évalue l'indice de risque basé sur l'exposition à la volatilité et aux erreurs.
    - Valeur forte : Indique un faible risque.
    - Valeur faible : Indique un risque élevé.

    Les variables utilisées sont :
    - total_volatility_exposure : Exposition à la volatilité.
    - total_error_exposure : Exposition aux erreurs.
    - total_gas_volatility_exposure : Exposition à la volatilité des coûts de gaz.

    Une valeur forte est souhaitable car elle indique un faible risque.
    """
    features['risk_index'] = features['total_volatility_exposure'] +  features['total_gas_volatility_exposure'] + features['total_error_exposure']

    # Opportuniy Score
    """
    Calcule un score d'opportunité basé sur l'exposition au volume, à la liquidité et à l'activité.
    - Valeur forte : Indique de nombreuses opportunités de marché.
    - Valeur faible : Indique peu d'opportunités ou un marché stagnant.

    Les variables utilisées sont :
    - total_volume_exposure : Exposition au volume total des transactions.
    - total_liquidity_exposure : Exposition à la liquidité.
    - total_activity_exposure : Exposition à l'activité.

    Une valeur forte est souhaitable car elle indique de nombreuses opportunités.
    """
    features['opportunity_score'] = (features['total_volume_exposure'] +
                                     features['total_liquidity_exposure'] +
                                     features['total_activity_exposure'])

    # Performance index
    """
    Évalue l'indice de performance basé sur le ratio entre l'exposition globale au marché et l'indice de risque.
    - Valeur forte : Indique une performance élevée par rapport au risque.
    - Valeur faible : Indique une performance faible par rapport au risque.

    Les variables utilisées sont :
    - Global_market_exposure_score : Score global d'exposition au marché.
    - Risk_index : Indice de risque.

    Une valeur forte est souhaitable car elle indique une performance élevée.
    """
    features['performance_index'] = (features['global_market_exposure_score'] /
                                     features['risk_index'])

    # Adoption Activity Score
    """
    Mesure le score d'activité d'adoption basé sur l'exposition à l'activité et à l'adoption des utilisateurs.
    - Valeur forte : Indique une forte adoption et activité des utilisateurs.
    - Valeur faible : Indique une faible adoption ou activité limitée des utilisateurs.

    Les variables utilisées sont :
    - total_activity_exposure : Exposition à l'activité.
    - total_user_adoption_exposure : Exposition à l'adoption par les utilisateurs.

    Une valeur forte est souhaitable car elle indique une forte adoption.
    """
    features['adoption_activity_score'] = (features['total_activity_exposure'] +
                                           features['total_user_adoption_exposure'])

    # Stability Index
    """
    Évalue l'indice de stabilité basé sur l'inverse de l'exposition à la volatilité et aux erreurs.
    - Valeur forte : Indique une grande stabilité.
    - Valeur faible : Indique une faible stabilité ou une forte volatilité.

    Les variables utilisées sont :
    - total_volatility_exposure : Exposition à la volatilité.
    - total_error_exposure : Exposition aux erreurs.

    Une valeur forte est souhaitable car elle indique une grande stabilité.
    """
    features['stability_index'] = (1 / (features['total_volatility_exposure'] +
                                        features['total_error_exposure']))

    # Volatility Exposure
    """
    Mesure l'exposition à la volatilité basée sur divers facteurs.
    - Valeur forte : Indique une faible exposition à la volatilité.
    - Valeur faible : Indique une forte exposition à la volatilité.

    Les variables utilisées sont :
    - total_volatility_exposure : Exposition à la volatilité.
    - total_gas_volatility_exposure : Exposition à la volatilité des coûts de gaz.
    - total_error_volatility_exposure : Exposition à la volatilité des erreurs.

    Une valeur forte est souhaitable car elle indique une faible exposition à la volatilité.
    """
    features['total_volatility_exposure_normalized'] = features['total_volatility_exposure'] / features['total_volatility_exposure'].max()
    features['total_gas_volatility_exposure_normalized'] = features['total_gas_volatility_exposure'] / features['total_gas_volatility_exposure'].max()
    features['total_error_volatility_exposure_normalized'] = features['total_error_volatility_exposure'] / features['total_error_volatility_exposure'].max()
    features['volatility_exposure'] = ((1 - features['total_volatility_exposure_normalized']) +
                                       (1 - features['total_gas_volatility_exposure_normalized']) +
                                       (1 - features['total_error_volatility_exposure_normalized']))

    # Market Influence
    """
    Évalue l'influence sur le marché basée sur un score de "baleine" (whale).
    - Valeur forte : Indique une forte influence sur le marché.
    - Valeur faible : Indique une faible influence ou une influence limitée sur le marché.

    La variable utilisée est :
    - whale_score : Score indiquant l'influence sur le marché.

    Une valeur forte est souhaitable car elle indique une forte influence sur le marché.
    """
    features['market_influence'] = features['whale_score']

    return features