import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

PROTOCOL_NAME_COLORS = {
    "Curve DAO": "#3399FF",   # DEX - Bleu
    "Uniswap": "#007ACC",     # DEX - Bleu
    "Balancer": "#005BBB",    # DEX - Bleu

    "Aave": "#DC143C",        # Lending - Vert
    "Maker": "#CC3300",       # Lending - Rouge

    "Tether": "#99FF99",  # Stablecoin - Vert menthe
    "USDC": "#33CC99",  # Stablecoin - Vert émeraude
    "Dai": "#00CC66",  # Stablecoin - Vert pomme

    "yearn.finance": "#FFCC00",     # Yield Farming - Jaune/Orange
    "Harvest Finance": "#FF9900",   # Yield Farming - Jaune/Orange

    "NFTFI": "#c24ee2",       # NFT - Rouge
}

PROTOCOL_TYPE_COLORS = {
    'DEX': "#007ACC",         # Uniswap (Green)
    'Lending': "#DC143C",     # Aave (Royal Blue)
    'Stablecoin': "#00CC66",  # Tether (Pink)
    'Yield Farming': "#FFCC00",   # Maker (Gold)
    'NFT-Fi': "#c24ee2",      # NFTFI (Red-Orange)
}

PROTOCOL_ORDER = [
    "Curve DAO", "Uniswap", "Balancer",  # DEX
    "Aave", "Maker",                     # Lending
    "Tether", "USDC", "Dai",             # Stablecoin
    "yearn.finance", "Harvest Finance",  # Yield Farming
    "NFTFI"                              # NFT
]

class TransactionAnalyzer:
    def __init__(self, df):
        self.df = df
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df.set_index('timestamp', inplace=True)

    def plot_tx_by_freq(self, freq, file_name, base_path, group):
        grouped = self.df.groupby([pd.Grouper(freq=freq), group])['transaction_hash'].nunique().unstack()
        self._plot_stacked_bar(grouped, file_name, base_path, group)

    def plot_value_by_freq(self, freq, file_name, base_path, group, value):
        grouped = self.df.groupby([pd.Grouper(freq=freq), group])[value].sum().unstack()
        self._plot_stacked_bar(grouped, file_name, base_path, group)

    def _plot_stacked_bar(self, grouped, file_name, base_path, group):
        """ Plot a stacked bar chart of the grouped data by month """
        grouped = grouped.fillna(0)
        grouped_normalized = grouped.div(grouped.sum(axis=1), axis=0) * 100
        colors = PROTOCOL_NAME_COLORS if group == 'protocol_name' else PROTOCOL_TYPE_COLORS
        if group == 'protocol_name':
            grouped_normalized = grouped_normalized[PROTOCOL_ORDER]

        plt.figure(figsize=(16, 8))
        plt.title(f'Stacked Bar Chart of {group.replace("_", " ").title()} Proportion by Month', pad=50, fontsize=14)
        ax = grouped_normalized.plot(
            kind='bar', stacked=True,
            color=[colors[col] for col in grouped_normalized.columns],
            ax=plt.gca(),
            width=0.75
        )
        ax.set_xlabel('Time')
        ax.set_ylabel('Proportion (%)')
        ax.legend(title=group.replace("_", " ").title(), loc='upper left', bbox_to_anchor=(1.06, 0.9))
        ax.set_xticklabels([pd.to_datetime(x).strftime('%b-%y') for x in grouped_normalized.index], rotation=45)
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 25, 50, 75, 100])

        for idx, (total, _) in enumerate(zip(grouped.sum(axis=1), grouped_normalized.iterrows())):
            if total >= 1e9:
                value_str = f'{total / 1e9:.2f}B'
            else:
                value_str = f'{total / 1e6:.2f}M'
            ax.text(idx, 101, value_str, ha='center', va='bottom', fontsize=10, color='black', rotation=45)

        # ---

        totals = grouped.sum(axis=1)

        ax2 = ax.twinx()
        ax2.plot(range(len(totals)), totals, color='black', marker='o', linestyle='-', linewidth=2,
                 label='Total')

        x = np.arange(len(totals))
        z = np.polyfit(x, totals, 1)
        p = np.poly1d(z)

        ax2.plot(x, p(x), color='black', linestyle='--', linewidth=2, label='Trend')

        trend_type = "positive" if z[0] > 0 else "négative"
        trend_label = f'Trend: y = {z[0]:.2f}x + {z[1]:.2f} ({trend_type})'
        ax2.text(0.7, 0.6, trend_label, transform=ax2.transAxes, fontsize=12,
                 verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.5))

        ax2.set_ylabel('Total')
        ax2.set_ylim(min(totals), totals.max() * 1.1)
        ax2.set_yscale('log')

        ax.set_xlim(-0.5, len(grouped) - 0.5)
        ax2.set_xlim(-0.5, len(grouped) - 0.5)

        ax2.tick_params(axis='y')
        ax2.spines['right'].set_position(('outward', 1))
        ax2.legend(loc='upper right', bbox_to_anchor=(1.14, 1))

        # ---

        plt.subplots_adjust(left=0.05, right=0.85, top=0.85, bottom=0.15)
        plt.savefig(f'{base_path}/{file_name}')
        plt.close()