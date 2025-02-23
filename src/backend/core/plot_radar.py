import numpy as np
import matplotlib.pyplot as plt

def plot_radar_chart(user_data, to_plot=None):


    metrics_names = [metric['name'].replace("_", " ").title() for metric in user_data['performances']]
    cluster_ranks = [metric[to_plot] for metric in user_data['performances']]

    metrics_names.append(metrics_names[0])
    cluster_ranks.append(cluster_ranks[0])

    angles = np.linspace(0, 2 * np.pi, len(metrics_names))
    fig, ax = plt.subplots(figsize=(20, 14), subplot_kw=dict(polar=True))

    ax.fill(angles, cluster_ranks, color='blue', alpha=0.25)
    ax.plot(angles, cluster_ranks, color='blue', linewidth=2)

    ax.set_thetagrids(np.degrees(angles), metrics_names)

    plt.title(f'Radar plot of {to_plot.replace("_", " ").title()}')
    plt.tight_layout()
    return fig

COLORS = [
    "vert: "#00FF00"
]