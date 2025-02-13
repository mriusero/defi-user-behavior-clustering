import time
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import export_image
from pyarrow import feather
import colorcet as cc
import matplotlib.pyplot as plt
import hashlib
from sklearn.decomposition import PCA
import seaborn as sns

base_path = "docs/graphics/exploratory_analysis/"

def time_taken(start, step_name):
    """Display the elapsed time for a given step."""
    elapsed_time = time.time() - start
    print(f"{step_name} took {elapsed_time:.2f} seconds.\n")

def load_data(file_path):
    """Load data from a feather file and convert it to a pandas DataFrame."""
    print("-- Data loading --")
    start = time.time()
    table = feather.read_table(file_path)
    features = table.to_pandas()
    time_taken(start, "Data loading")
    return features

def calculate_transaction_activity(df):
    """Calculate the number of transactions for each address."""
    print("-- Calculating transaction activity --")
    start = time.time()
    df['nb_transactions'] = df['received_count'] + df['sent_count']
    time_taken(start, "Calculating transaction activity")

def encode_addresses(df):
    """Encode addresses using SHA-256 hashing."""
    print("-- Encoding addresses --")
    start = time.time()
    df['address_hash'] = df['address'].apply(lambda x: int(hashlib.sha256(x.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
    time_taken(start, "Encoding addresses")

def plot_heatmap(df, x, y, heat, filename):
    """Create and save a exploratory_analysis using datashader."""
    print(f"-- Creating {filename} exploratory_analysis --")
    start = time.time()
    cvs = ds.Canvas(plot_width=500, plot_height=500, x_axis_type='linear', y_axis_type='linear')
    img = tf.shade(cvs.points(df, x, y, ds.mean(heat)), cmap=cc.fire, how='eq_hist')

    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.imshow(img.to_pil(), aspect='auto')
    ax.set_title(filename)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.invert_yaxis()
    ax.set_facecolor('white')

    plt.savefig(f"{base_path}{filename}.png", bbox_inches='tight', facecolor='white')
    plt.close(fig)
    time_taken(start, f"Exporting {filename}")

def categorize_protocol(row):
    """Categorize protocol types based on boolean columns."""
    categories = []
    if row['type_dex']:
        categories.append('DEX')
    if row['type_lending']:
        categories.append('Lending')
    if row['type_stablecoin']:
        categories.append('Stablecoin')
    if row['type_yield_farming']:
        categories.append('Yield Farming')
    if row['type_nft_fi']:
        categories.append('NFT-Fi')
    return tuple(sorted(categories))

def plot_pairplot_pca(df):
    """Perform PCA and plot a pairplot of the reduced features."""
    print("-- Pair plot PCA --")
    start = time.time()
    df = df.sample(100000, random_state=42).drop(columns=['address']).fillna(0)
    df['protocol_type'] = df.apply(categorize_protocol, axis=1)
    df['protocol_type'] = df['protocol_type'].astype('category')
    protocol_type_codes = df['protocol_type'].cat.codes

    pca = PCA(n_components=28)
    features_reduced = pca.fit_transform(df.drop(columns=['protocol_type']))
    features_reduced = pd.DataFrame(features_reduced)
    features_reduced['protocol_type'] = protocol_type_codes

    sns.pairplot(features_reduced, hue='protocol_type', palette='viridis')
    plt.savefig(f"{base_path}pairplot_pca.png", bbox_inches='tight', facecolor='white')
    time_taken(start, "Pairplot PCA")

def main():
    features = load_data("data/features/features_standardised.arrow")
    calculate_transaction_activity(features)
    encode_addresses(features)

    plot_heatmap(features, 'received_count', 'sent_count', 'nb_transactions', 'transactions_numbers')
    plot_heatmap(features, 'total_received_eth', 'total_sent_eth', 'net_flow_eth', 'transactions_values')

    plot_pairplot_pca(features)

if __name__ == "__main__":
    main()
