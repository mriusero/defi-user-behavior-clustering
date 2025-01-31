# Statistical Analysis of Numeric Variables

## Summary of Results

| Variable | Normality Test | Skewness | Kurtosis | Recommended Standardization |
|----------|----------------|----------|----------|----------------------------|
| `received_count` | Not-normal | 636.27 → Positively skewed | 542539.88 → Leptokurtic | Logarithmic transformation |
| `total_received_eth` | Not-normal | 1172.76 → Positively skewed | 1375364.00 → Leptokurtic | Logarithmic transformation |
| `sent_count` | Not-normal | 600.69 → Positively skewed | 455850.90 → Leptokurtic | Logarithmic transformation |
| `total_sent_eth` | Not-normal | 1172.76 → Positively skewed | 1375364.00 → Leptokurtic | Logarithmic transformation |
| `type_dex` | Not-normal | 1062.98 → Positively skewed | 1333750.53 → Leptokurtic | Logarithmic transformation |
| `type_lending` | Not-normal | 2138.04 → Positively skewed | 5069083.65 → Leptokurtic | Logarithmic transformation |
| `type_stablecoin` | Not-normal | 665.88 → Positively skewed | 631838.05 → Leptokurtic | Logarithmic transformation |
| `type_yield_farming` | Not-normal | 1603.56 → Positively skewed | 3158498.58 → Leptokurtic | Logarithmic transformation |
| `type_nft_fi` | Not-normal | 1608.27 → Positively skewed | 2860517.87 → Leptokurtic | Logarithmic transformation |
| `curve_dao_count` | Not-normal | 1104.51 → Positively skewed | 1408833.88 → Leptokurtic | Logarithmic transformation |
| `aave_count` | Not-normal | 1160.15 → Positively skewed | 1864632.70 → Leptokurtic | Logarithmic transformation |
| `tether_count` | Not-normal | 807.99 → Positively skewed | 881850.41 → Leptokurtic | Logarithmic transformation |
| `uniswap_count` | Not-normal | 879.60 → Positively skewed | 1021695.50 → Leptokurtic | Logarithmic transformation |
| `maker_count` | Not-normal | 2223.42 → Positively skewed | 5356492.38 → Leptokurtic | Logarithmic transformation |
| `yearn_finance_count` | Not-normal | 1685.00 → Positively skewed | 3399699.39 → Leptokurtic | Logarithmic transformation |
| `usdc_count` | Not-normal | 787.54 → Positively skewed | 849307.80 → Leptokurtic | Logarithmic transformation |
| `dai_count` | Not-normal | 1406.96 → Positively skewed | 2603506.52 → Leptokurtic | Logarithmic transformation |
| `balancer_count` | Not-normal | 853.39 → Positively skewed | 1011212.00 → Leptokurtic | Logarithmic transformation |
| `harvest_finance_count` | Not-normal | 1485.72 → Positively skewed | 2586003.26 → Leptokurtic | Logarithmic transformation |
| `nftfi_count` | Not-normal | 1608.27 → Positively skewed | 2860517.87 → Leptokurtic | Logarithmic transformation |
| `protocol_type_diversity` | Not-normal | 18.40 → Positively skewed | 344.43 → Leptokurtic | Logarithmic transformation |
| `protocol_name_diversity` | Not-normal | 16.11 → Positively skewed | 297.87 → Leptokurtic | Logarithmic transformation |
| `net_flow_eth` | Not-normal | 2051.03 → Positively skewed | 4479798.36 → Leptokurtic | Logarithmic transformation |
| `whale_score` | Not-normal | 1098.78 → Positively skewed | 1231028.50 → Leptokurtic | Logarithmic transformation |
| `min_sent_eth` | Not-normal | 1172.76 → Positively skewed | 1375364.00 → Leptokurtic | Logarithmic transformation |
| `avg_sent_eth` | Not-normal | 1172.14 → Positively skewed | 1374369.19 → Leptokurtic | Logarithmic transformation |
| `med_sent_eth` | Not-normal | 1172.76 → Positively skewed | 1375364.00 → Leptokurtic | Logarithmic transformation |
| `max_sent_eth` | Not-normal | 927.15 → Positively skewed | 859600.63 → Leptokurtic | Logarithmic transformation |
| `std_sent_eth` | Not-normal | 1754.70 → Positively skewed | 3223966.68 → Leptokurtic | Logarithmic transformation |
| `min_sent_gas` | Not-normal | 22.95 → Positively skewed | 2554.70 → Leptokurtic | Logarithmic transformation |
| `avg_sent_gas` | Not-normal | 18.67 → Positively skewed | 1681.49 → Leptokurtic | Logarithmic transformation |
| `med_sent_gas` | Not-normal | 20.79 → Positively skewed | 2103.01 → Leptokurtic | Logarithmic transformation |
| `max_sent_gas` | Not-normal | 30.08 → Positively skewed | 2500.09 → Leptokurtic | Logarithmic transformation |
| `std_sent_gas` | Not-normal | 38.23 → Positively skewed | 3971.56 → Leptokurtic | Logarithmic transformation |
| `avg_gas_efficiency_sent` | Not-normal | 1172.14 → Positively skewed | 1374369.19 → Leptokurtic | Logarithmic transformation |
| `peak_hour_sent` | Not-normal | 0.59 → Positively skewed | -0.99 → Platykurtic | No transformation needed |
| `peak_count_sent` | Not-normal | 913.03 → Positively skewed | 1266787.15 → Leptokurtic | Logarithmic transformation |
| `tx_frequency_sent` | Not-normal | 54.18 → Positively skewed | 4234.75 → Leptokurtic | Logarithmic transformation |
| `min_received_eth` | Not-normal | 1172.76 → Positively skewed | 1375364.00 → Leptokurtic | Logarithmic transformation |
| `avg_received_eth` | Not-normal | 1171.37 → Positively skewed | 1373116.36 → Leptokurtic | Logarithmic transformation |
| `med_received_eth` | Not-normal | 1172.76 → Positively skewed | 1375364.00 → Leptokurtic | Logarithmic transformation |
| `max_received_eth` | Not-normal | 927.15 → Positively skewed | 859600.63 → Leptokurtic | Logarithmic transformation |
| `std_received_eth` | Not-normal | 1728.17 → Positively skewed | 3095092.87 → Leptokurtic | Logarithmic transformation |
| `min_received_gas` | Not-normal | 20.67 → Positively skewed | 1468.72 → Leptokurtic | Logarithmic transformation |
| `avg_received_gas` | Not-normal | 19.30 → Positively skewed | 1265.55 → Leptokurtic | Logarithmic transformation |
| `med_received_gas` | Not-normal | 19.83 → Positively skewed | 1332.59 → Leptokurtic | Logarithmic transformation |
| `max_received_gas` | Not-normal | 23.32 → Positively skewed | 1530.42 → Leptokurtic | Logarithmic transformation |
| `std_received_gas` | Not-normal | 39.41 → Positively skewed | 3819.20 → Leptokurtic | Logarithmic transformation |
| `avg_gas_efficiency_received` | Not-normal | 1171.37 → Positively skewed | 1373116.36 → Leptokurtic | Logarithmic transformation |
| `peak_hour_received` | Not-normal | 0.47 → Symmetric | -1.16 → Platykurtic | Min-Max normalization |
| `peak_count_received` | Not-normal | 596.68 → Positively skewed | 556336.25 → Leptokurtic | Logarithmic transformation |
| `tx_frequency_received` | Not-normal | 54.01 → Positively skewed | 4263.63 → Leptokurtic | Logarithmic transformation |
| `total_volume_exposure` | Not-normal | 806.32 → Positively skewed | 879343.66 → Leptokurtic | Logarithmic transformation |
| `total_volatility_exposure` | Not-normal | 1437.17 → Positively skewed | 2391825.62 → Leptokurtic | Logarithmic transformation |
| `total_gas_exposure` | Not-normal | 778.60 → Positively skewed | 797771.97 → Leptokurtic | Logarithmic transformation |
| `total_error_exposure` | Normal | nan → Negatively skewed | nan → Platykurtic | Z-score normalization |
| `total_liquidity_exposure` | Not-normal | 1160.15 → Positively skewed | 1864632.70 → Leptokurtic | Logarithmic transformation |
| `total_activity_exposure` | Not-normal | 712.78 → Positively skewed | 724723.90 → Leptokurtic | Logarithmic transformation |
| `total_user_adoption_exposure` | Not-normal | 744.99 → Positively skewed | 779257.40 → Leptokurtic | Logarithmic transformation |
| `total_gas_volatility_exposure` | Not-normal | 911.47 → Positively skewed | 1045815.34 → Leptokurtic | Logarithmic transformation |
| `total_error_volatility_exposure` | Not-normal | 1160.15 → Positively skewed | 1864632.70 → Leptokurtic | Logarithmic transformation |
| `total_high_value_exposure` | Not-normal | 1160.15 → Positively skewed | 1864632.70 → Leptokurtic | Logarithmic transformation |
