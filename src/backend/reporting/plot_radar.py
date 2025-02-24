import numpy as np
import matplotlib.pyplot as plt


def upper_and_lower_bounds(ranks):
    """ Compute upper and lower bounds for radar chart """
    bounds = {}
    for col in ranks.columns:
        if col.endswith('_global_rank') or col.endswith('_cluster_rank'):
            bounds[col] = {
                'lower_median': ranks[col].quantile(0.25),
                'upper_median': ranks[col].quantile(0.75),
        #        'max': ranks[col].max(),
            }
    return bounds


def plot_radar_chart(bounds, user_data, to_plot='global_rank'):
    metrics_names = [metric['name'].replace("_", " ").title() for metric in user_data['performances']]
    cluster_ranks = [metric[to_plot] for metric in user_data['performances']]

    lower_medians = [bounds[metric['name'] + '_' + to_plot]['lower_median'] for metric in user_data['performances']]
    upper_medians = [bounds[metric['name'] + '_' + to_plot]['upper_median'] for metric in user_data['performances']]
  #  maxs = [bounds[metric['name'] + '_' + to_plot]['max'] for metric in user_data['performances']]

    metrics_names.append(metrics_names[0])
    cluster_ranks.append(cluster_ranks[0])
    lower_medians.append(lower_medians[0])
    upper_medians.append(upper_medians[0])
  #  maxs.append(maxs[0])

    angles = np.linspace(0, 2 * np.pi, len(metrics_names))
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(polar=True))

    ax.fill(angles, cluster_ranks, color='blue', alpha=0.25)
    ax.plot(angles, cluster_ranks, color='blue', linewidth=2)

    ax.fill(angles, lower_medians, color='red', alpha=0.25)
    ax.plot(angles, lower_medians, color='red', linewidth=2, linestyle='--', label='Lower Medians')

    ax.fill(angles, upper_medians, color='lightgreen', alpha=0.25)
    ax.plot(angles, upper_medians, color='green', linewidth=2, linestyle='--', label='Upper Medians')

  #  ax.fill(angles, maxs, color='silver', alpha=0.25)
  #  ax.plot(angles, maxs, color='Green', linewidth=2, linestyle='-', label='Maxs')

    ax.set_rgrids([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], fontsize=8)
    ax.set_thetagrids(np.degrees(angles), metrics_names, fontsize=10)

    ax.legend()
    fig.subplots_adjust(top=0.80)
    plt.tight_layout()

    return fig