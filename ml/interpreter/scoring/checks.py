import numpy as np
import matplotlib.pyplot as plt


def check_scores(df):
    """
    Check the scores calculated for the users :
        - Check if the scores are above 0
        - Check if there are NaN or Inf values in the scores
    """
    out_of_bounds = {}
    nan_inf_columns = {}

    for column in df.columns:
        count_out_of_bounds = (df[column] < 0).sum()
        count_nan_inf = df[column].isna().sum() + np.isinf(df[column]).sum()

        if count_out_of_bounds > 0:
            out_of_bounds[column] = count_out_of_bounds

        if count_nan_inf > 0:
            nan_inf_columns[column] = count_nan_inf

    return out_of_bounds, nan_inf_columns


def analyze_distribution(df):
    """ Analyze the distribution of the scores """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

    # Histogram of global_score
    axes[0].hist(df['global_score'], bins=30, edgecolor='black', alpha=0.7, color='skyblue')
    axes[0].axvline(df['global_score'].mean(), color='red', linestyle='dashed', linewidth=1, label='Moyenne')
    axes[0].set_title('Histogram of Global_score', fontsize=15)
    axes[0].set_xlabel('Global_score', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].legend()
    axes[0].grid(True)

    # Histogram of global_score_global_rank
    axes[1].hist(df['global_score_global_rank'], bins=30, edgecolor='black', alpha=0.7, color='salmon')
    axes[1].axvline(df['global_score_global_rank'].mean(), color='red', linestyle='dashed', linewidth=1, label='Moyenne')
    axes[1].set_title('Histogram of Global_score_global_rank', fontsize=15)
    axes[1].set_xlabel('Global_score_global_rank', fontsize=12)
    axes[1].set_ylabel('Frequency', fontsize=12)
    axes[1].legend()
    axes[1].grid(True)

    # Histogram of global_score_cluster_rank
    axes[2].hist(df['global_score_cluster_rank'], bins=30, edgecolor='black', alpha=0.7, color='lightgreen')
    axes[2].axvline(df['global_score_cluster_rank'].mean(), color='red', linestyle='dashed', linewidth=1, label='Moyenne')
    axes[2].set_title('Histogram of Global_score_cluster_rank', fontsize=15)
    axes[2].set_xlabel('Global_score_cluster_rank', fontsize=12)
    axes[2].set_ylabel('Frequency', fontsize=12)
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()