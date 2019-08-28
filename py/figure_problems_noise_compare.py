import matplotlib.pyplot as plt
import seaborn as sns
import os

import numpy as np
import matlab_utils as mlu
import plot_utils as plu
import settings as settings

# noise_types = ['White', 'Pink', 'Brown']
noise_types = ['Brown']



def figure_problemns_noise_compare(noise_type, filename_format):
    """
    Savepath should be a string with {noise_type} to fill a lowercase name of the noise in
    :param savepath:
    :return:
    """
    noise_examples = mlu.loadmat('./mat/noise_examples.mat')

    Fs = 20  # Sampling rate: samples/millisecond
    T = 1000  # plot T seconds of noise

    noise_example = noise_examples[noise_type]

    n = len(noise_example)  # Number of points

    x = np.linspace(0, T, T*Fs)


    fig, ax = plt.subplots()
    for region in [0, 1]:
        y = noise_example[region][0:T * Fs]
        sns.lineplot(x, y, ax=ax, label=f"Noise to region {region+1}")

    ax.set_ylim([-1.2, 1.2])
    ax.legend(loc='upper left')

    # ax.set_title(f"{noise_type} noise")

    ax.set_xlabel("Time t in $ms$")
    ax.set_ylabel("$I_{noise}$ in $\mu A/cm^2$")

    fig.show()

    if filename_format:
        filename = filename_format.format(noise_type=noise_type.lower())
        plu.save_figure(fig, filename, noise_type=noise_type, source='FigureMethodsNoiseExamples.m')


def save_default():
    for noise_type in noise_types:
        figure_problemns_noise_compare(noise_type=noise_type, filename_format='figure_problems_noise_{noise_type}.png')


if __name__ == "__main__":
    save_default()