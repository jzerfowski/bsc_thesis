import matplotlib.pyplot as plt
import seaborn as sns
import os

import numpy as np
import matlab_utils as mlu
import plot_utils as plu
import settings as settings

filename_format = 'figure_problems_noise_{noise_type}_correlation_histogram.png'

noise_white_correlations = mlu.loadmat('./mat/noise_correlations_white.mat')['correlations']
noise_pink_correlations = mlu.loadmat('./mat/noise_correlations_pink.mat')['correlations']
noise_brown_correlations = mlu.loadmat('./mat/noise_correlations_brown.mat')['correlations']

noise_types = {
        'white': {'correlations': noise_white_correlations,
                  'title': 'White noise', },
        'pink': {'correlations': noise_pink_correlations,
                 'title': 'Pink noise'},
        'brown': {'correlations': noise_brown_correlations,
                  'title': 'Brown noise', },
    }


def figure_problems_noise_correlations_histogram(noise_type, noise_info, filename_format=None):
    """Savepath should be a string with {noise_type} to fill in a lowercase name of the noise"""
    correlation_threshold = 0.05

    correlation = noise_info['correlations']
    title = noise_info['title']

    ratio = sum(abs(correlation) <= correlation_threshold) / len(correlation)

    print(f"Details about {noise_info['title']}:")
    print(f"n = {len(correlation)}")
    print(f"mean = {np.mean(correlation)}, var = {np.var(correlation)}")
    print(f"{ratio * 100}% of the correlations are below the threshold of {correlation_threshold}")

    num_bins = 400
    stepwidth = 2 / num_bins
    noise_histogram, bins = np.histogram(correlation, bins=num_bins, range=(-1, 1))

    fig, ax = plt.subplots(figsize=(5.0, 3.8))
    ax.bar(x=bins[:-1] + stepwidth, height=noise_histogram, width=stepwidth)

    ax.set_xlabel('Correlation')

    ax.set_ylabel('Count / 0.005')
    # ax.set_title(title)

    fig.show()

    if filename_format:
        filename = filename_format.format(noise_type=noise_type.lower())
        plu.save_figure(fig, filename, noise_type=noise_type,
                        samples=len(correlation),
                        correlation_threshold=correlation_threshold,
                        below_threshold=ratio,
                        correlation_source="FigureMethodsNoiseCorrelations.m")


def save_default():
    for noise_type, noise_info in noise_types.items():
        figure_problems_noise_correlations_histogram(noise_type=noise_type, noise_info=noise_info, filename_format=filename_format)


if __name__ == "__main__":
    save_default()
