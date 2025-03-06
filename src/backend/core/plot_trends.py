import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns

plt.style.use('default')

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
        # Delete transactions of 'gouvernance transfer' = no value transferred (15 tx identified)
        print("-------------------------")

        top_10_indices = self.df.nlargest(15, 'value (ETH)').index
        self.df = self.df.drop(top_10_indices)

        total_rows = len(self.df)
        protocol_counts = self.df[group].value_counts()
        protocol_proportions = protocol_counts / total_rows

        print("Protocoles uniques et leurs proportions :")
        for protocol, proportion in protocol_proportions.items():
            print(f"{protocol}: {proportion:.2%}")

        grouped = self.df.groupby([pd.Grouper(freq=freq), group])[value].sum().unstack()
        self._plot_stacked_bar(grouped, file_name, base_path, group)

    def plot_senders_by_freq(self, freq, file_name, base_path, group):
        grouped = self.df.groupby([pd.Grouper(freq=freq), group])['from'].nunique().unstack()
        self._plot_stacked_bar(grouped, file_name, base_path, group)

    def plot_receivers_by_freq(self, freq, file_name, base_path, group):
        grouped = self.df.groupby([pd.Grouper(freq=freq), group])['to'].nunique().unstack()
        self._plot_stacked_bar(grouped, file_name, base_path, group)

    def plot_users_by_freq(self, freq, file_name, base_path, group):
        senders_grouped = self.df.groupby([pd.Grouper(freq=freq), group])['from'].nunique().unstack()
        receivers_grouped = self.df.groupby([pd.Grouper(freq=freq), group])['to'].nunique().unstack()
        combined_grouped = senders_grouped.add(receivers_grouped, fill_value=0)
        self._plot_stacked_bar(combined_grouped, file_name, base_path, group)

    def plot_tx_vs_users_scatter(self, freq, file_name, base_path, group):
        tx_count = self.df.groupby([pd.Grouper(freq=freq), group])['transaction_hash'].nunique().unstack()
        users_count = self.df.groupby([pd.Grouper(freq=freq), group])['from'].nunique().unstack().add(
            self.df.groupby([pd.Grouper(freq=freq), group])['to'].nunique().unstack(), fill_value=0
        )
        plt.style.use('default')
        plt.figure(figsize=(10, 6))

        colors = PROTOCOL_NAME_COLORS if group == 'protocol_name' else PROTOCOL_TYPE_COLORS

        all_tx = tx_count.sum(axis=1).dropna().values.reshape(-1, 1)
        all_users = users_count.sum(axis=1).dropna().values

        global_model = LinearRegression()
        global_model.fit(all_tx, all_users)
        global_trend_line = global_model.predict(all_tx)

        correlation_matrix = np.corrcoef(all_tx.flatten(), all_users)
        correlation_coefficient = correlation_matrix[0, 1]

        for protocol in tx_count.columns:
            if protocol in users_count.columns:
                plt.scatter(tx_count[protocol], users_count[protocol],
                            color=colors.get(protocol, 'gray'),
                            label=protocol, alpha=0.6)

        plt.plot(all_tx, global_trend_line, color='black', linestyle='--', label='Global Trend', alpha=0.2)

        trend_type = "positive" if global_model.coef_[0] > 0 else "négative"
        trend_label = f'Trend: y = {global_model.coef_[0]:.2f}x + {global_model.intercept_:.2f} ({trend_type})\nCorrelation: {correlation_coefficient:.2f}'

        plt.text(0.97, 0.15, trend_label, transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(facecolor='white', alpha=0.5))

        plt.title(f'Correlation between number of transactions and number of users ({freq})', pad=20)
        plt.xlabel('Number of transactions')
        plt.ylabel('Number of users')
        plt.legend(title='Protocol')
        plt.grid(True)
        plt.savefig(f'{base_path}/{file_name}')

    def plot_senders_vs_receivers_scatter(self, freq, file_name, base_path, group):
        senders_count = self.df.groupby([pd.Grouper(freq=freq), group])['from'].nunique().unstack()
        receivers_count = self.df.groupby([pd.Grouper(freq=freq), group])['to'].nunique().unstack()

        plt.style.use('default')
        plt.figure(figsize=(10, 6))

        colors = PROTOCOL_NAME_COLORS if group == 'protocol_name' else PROTOCOL_TYPE_COLORS

        all_senders = senders_count.sum(axis=1).dropna().values.reshape(-1, 1)
        all_receivers = receivers_count.sum(axis=1).dropna().values

        global_model = LinearRegression()
        global_model.fit(all_senders, all_receivers)
        global_trend_line = global_model.predict(all_senders)

        correlation_matrix = np.corrcoef(all_senders.flatten(), all_receivers)
        correlation_coefficient = correlation_matrix[0, 1]

        for protocol in senders_count.columns:
            if protocol in receivers_count.columns:
                plt.scatter(senders_count[protocol], receivers_count[protocol],
                            color=colors.get(protocol, 'gray'),
                            label=protocol, alpha=0.6)

        plt.plot(all_senders, global_trend_line, color='black', linestyle='--', label='Global Trend', alpha=0.2)

        trend_type = "positive" if global_model.coef_[0] > 0 else "négative"
        trend_label = f'Trend: y = {global_model.coef_[0]:.2f}x + {global_model.intercept_:.2f} ({trend_type})\nCorrelation: {correlation_coefficient:.2f}'

        plt.text(0.97, 0.15, trend_label, transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(facecolor='white', alpha=0.5))

        plt.title(f'Correlation between number of senders and number of receivers ({freq})', pad=20)
        plt.xlabel('Number of senders')
        plt.ylabel('Number of receivers')
        plt.legend(title='Protocol')
        plt.grid(True)
        plt.savefig(f'{base_path}/{file_name}')

    def plot_users_vs_value_scatter(self, freq, file_name, base_path, group, value_column='value (ETH)'):
        # Delete transactions of 'gouvernance transfer' = no value transferred (15 tx identified)
        print("-------------------------")
        top_10_indices = self.df.nlargest(15, 'value (ETH)').index
        self.df = self.df.drop(top_10_indices)

        users_count = self.df.groupby([pd.Grouper(freq=freq), group])['from'].nunique().unstack().add(
            self.df.groupby([pd.Grouper(freq=freq), group])['to'].nunique().unstack(), fill_value=0
        )
        value_sum = self.df.groupby([pd.Grouper(freq=freq), group])[value_column].sum().unstack()

        plt.style.use('default')
        plt.figure(figsize=(10, 6))

        colors = PROTOCOL_NAME_COLORS if group == 'protocol_name' else PROTOCOL_TYPE_COLORS

        all_users = users_count.sum(axis=1).dropna().values.reshape(-1, 1)
        all_values = value_sum.sum(axis=1).dropna().values

        global_model = LinearRegression()
        global_model.fit(all_users, all_values)
        global_trend_line = global_model.predict(all_users)

        correlation_matrix = np.corrcoef(all_users.flatten(), all_values)
        correlation_coefficient = correlation_matrix[0, 1]

        for protocol in users_count.columns:
            if protocol in value_sum.columns:
                plt.scatter(users_count[protocol], value_sum[protocol],
                            color=colors.get(protocol, 'gray'),
                            label=protocol, alpha=0.6)

        plt.plot(all_users, global_trend_line, color='black', linestyle='--', label='Global Trend', alpha=0.2)

        trend_type = "positive" if global_model.coef_[0] > 0 else "négative"
        trend_label = f'Trend: y = {global_model.coef_[0]:.2f}x + {global_model.intercept_:.2f} ({trend_type})\nCorrelation: {correlation_coefficient:.2f}'

        plt.text(0.97, 0.15, trend_label, transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(facecolor='white', alpha=0.5))

        plt.title(f'Correlation between number of users and sum of {value_column} ({freq})', pad=20)
        plt.xlabel('Number of users')
        plt.ylabel(f'Sum of {value_column}')
        plt.legend(title='Protocol')
        plt.grid(True)
        plt.savefig(f'{base_path}/{file_name}')

    def plot_gas_vs_users_scatter(self, freq, file_name, base_path, group):
        gas_used = self.df.groupby([pd.Grouper(freq=freq), group])['gas_used'].sum().unstack()
        users_count = self.df.groupby([pd.Grouper(freq=freq), group])['from'].nunique().unstack().add(
            self.df.groupby([pd.Grouper(freq=freq), group])['to'].nunique().unstack(), fill_value=0
        )
        plt.style.use('default')
        plt.figure(figsize=(10, 6))

        colors = PROTOCOL_NAME_COLORS if group == 'protocol_name' else PROTOCOL_TYPE_COLORS

        all_gas = gas_used.sum(axis=1).dropna().values.reshape(-1, 1)
        all_users = users_count.sum(axis=1).dropna().values

        global_model = LinearRegression()
        global_model.fit(all_gas, all_users)
        global_trend_line = global_model.predict(all_gas)

        correlation_matrix = np.corrcoef(all_gas.flatten(), all_users)
        correlation_coefficient = correlation_matrix[0, 1]

        for protocol in gas_used.columns:
            if protocol in users_count.columns:
                plt.scatter(gas_used[protocol], users_count[protocol],
                            color=colors.get(protocol, 'gray'),
                            label=protocol, alpha=0.6)

        plt.plot(all_gas, global_trend_line, color='black', linestyle='--', label='Global Trend', alpha=0.2)

        trend_type = "positive" if global_model.coef_[0] > 0 else "négative"
        trend_label = f'Trend: y = {global_model.coef_[0]:.2f}x + {global_model.intercept_:.2f} ({trend_type})\nCorrelation: {correlation_coefficient:.2f}'

        plt.text(0.97, 0.15, trend_label, transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(facecolor='white', alpha=0.5))

        plt.title(f'Correlation between gas used and number of users ({freq})', pad=20)
        plt.xlabel('Gas used')
        plt.ylabel('Number of users')
        plt.legend(title='Protocol')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{base_path}/{file_name}')

    def plot_correlation_heatmap(self, freq, filename, base_path):
        grouped = self.df.groupby(pd.Grouper(freq=freq)).agg(
            senders=pd.NamedAgg(column='from', aggfunc='nunique'),
            receivers=pd.NamedAgg(column='to', aggfunc='nunique'),
            total_users=pd.NamedAgg(column='from', aggfunc=lambda x: x.nunique() + self.df['to'].nunique()),
            value_eth=pd.NamedAgg(column='value (ETH)', aggfunc='sum'),
            gas=pd.NamedAgg(column='gas', aggfunc='sum'),
            gas_used=pd.NamedAgg(column='gas_used', aggfunc='sum'),
            protocol=pd.NamedAgg(column='protocol_name', aggfunc='nunique'),
            type=pd.NamedAgg(column='type', aggfunc='nunique')
        )
        correlation_matrix = grouped.corr()
        plt.style.use('default')
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='viridis', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Heatmap of Transaction Variables')
        plt.tight_layout()
        plt.savefig(f'{base_path}/{filename}')


    def _plot_stacked_bar(self, grouped, file_name, base_path, group):
        """ Plot a stacked bar chart of the grouped data by month """
        grouped = grouped.fillna(0)
        grouped_normalized = grouped.div(grouped.sum(axis=1), axis=0) * 100
        colors = PROTOCOL_NAME_COLORS if group == 'protocol_name' else PROTOCOL_TYPE_COLORS
        if group == 'protocol_name':
            grouped_normalized = grouped_normalized[PROTOCOL_ORDER]

        plt.style.use('default')
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