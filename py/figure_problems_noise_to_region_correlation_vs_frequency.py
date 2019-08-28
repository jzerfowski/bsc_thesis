import pandas as pd

import matlab_utils as mlu

import seaborn as sns
import matplotlib.pyplot as plt
import os
import settings as settings
import numpy as np

import plot_utils as plu


def figure_problems_noise_to_region_correlation_vs_frequency(region_to, filename=None):
    noise_types = {
        'brown10': {'runnumbers': [117, 118, 122],
                    'title': "Strong Brown noise",
                    'color': '#572b0c',  # Saddle Brown
                    'style': '-',
                    },
        'brown05': {'runnumbers': [140, 134, 141],
                    'title': "Weak Brown noise",
                    'color': '#9c4e15',  # Saddle Brown
                    'style': '--',
                    },
        'pink': {'runnumbers': [112, 115, 114],
                 'title': "Pink noise",
                 'color': '#FF1493',  # Deep Pink
                 'style': '-.'
                 },
        'white': {'runnumbers': [123, 156, 157],
                  'title': "White noise",
                  'color': '#808080',  # Web Gray
                  'style': ':'
                  },
    }

    analysis_info2_name = f'rhos_fper_noise1_reg{region_to}'
    # analysis_info2_lag = f'{analysis_info2_name}_lag0'
    method = mlu.METHOD_CORRELATION_MAX

    fig, ax = plt.subplots()

    for noise_type, noise_details in noise_types.items():
        runnumbers = noise_details['runnumbers']

        correlation_dfs = [mlu.get_run_correlations(runnumber, method,
                                                    [analysis_info2_name])[analysis_info2_name] for runnumber in
                           runnumbers]

        correlation_mean_line = pd.concat(correlation_dfs).groupby(level=[0]).mean()

        print(f"Details about {noise_details['title']}:")
        print(f"Mean {np.mean(correlation_mean_line)}")

        noise_details['correlation_mean'] = np.mean(correlation_mean_line)

        ax.plot(correlation_mean_line, color=noise_details['color'], label=noise_details['title'],
                linestyle=noise_details['style'])

    ax.set_xlabel("Intrinsic frequency of region 1 ($Hz$)")
    ax.set_xticks(np.linspace(0, 39, 7))
    xticklabels = np.linspace(35, 65, 7)
    ax.set_xticklabels(xticklabels)

    ax.set_ylabel("Correlation")
    ax.set_ylim(-0.08, 1.02)

    # ax.set_title(f"Mean correlation between noise$_1$ and firing rate of region {region_to}")
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.92))

    fig.show()

    plu.save_figure(fig, filename, region_to=region_to, noise_types=noise_types)


def save_default():
    figure_problems_noise_to_region_correlation_vs_frequency(region_to=1,
                                                             filename='figure_problems_noise_to_region1_correlation.png')
    figure_problems_noise_to_region_correlation_vs_frequency(region_to=2,
                                                             filename='figure_problems_noise_to_region2_correlation.png')


if __name__ == "__main__":
    save_default()
