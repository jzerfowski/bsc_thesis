import matplotlib.pyplot as plt
import seaborn as sns
import os

import numpy as np
import matlab_utils as mlu
import plot_utils as plu
import settings as settings

runnumber = 134
run_frequency = 54.0541
l1 = 30
l2 = 10
data_source = './mat/noise_sigfreq_sigfper_example.mat'

filename = None
filename = 'figure_problems_shifting_window_noise_signal.png'


def norm_signal(sig):
    return (sig - np.min(sig)) / (np.max(sig) - np.min(sig))


def figure_problems_shifting_windows_noise_signal(runnumber, l1, l2, run_frequency, data_source, filename):
    noise_signal_dataset = mlu.loadmat(data_source)

    dthist = 0.5

    t_start = 0
    t_stop = 500

    noise_shift = int(1000 / (run_frequency * dthist))

    idx_stop = int(t_stop / dthist) + noise_shift

    sig_noise = noise_signal_dataset['sig_noise']
    sig_fper = noise_signal_dataset['sigfper']
    sig_freq = noise_signal_dataset['sigfreq']

    sig_noise1_norm = norm_signal(sig_noise[0, :idx_stop])
    sig_fper1_norm = norm_signal(sig_fper[:idx_stop, 0])
    sig_fper2_norm = norm_signal(sig_fper[:idx_stop, 1])
    sig_freq1_norm = norm_signal(sig_freq[:idx_stop, 0])
    sig_freq2_norm = norm_signal(sig_freq[:idx_stop, 1])

    n = len(sig_noise1_norm) - noise_shift
    t = n * dthist  # in ms

    x = np.linspace(0, t, n)

    factor = 3.5/6.5
    width = 8
    height = 8*factor
    fig, ax = plt.subplots(figsize=(10, 4.4))

    ax.plot(x, sig_noise1_norm[noise_shift:], color='#9c4e15', label=r'$\rm{Noise}_1$')
    ax.plot(x, sig_fper1_norm[noise_shift:], label='Region 1 Firing rate')
    ax.plot(x, sig_fper1_norm[:-noise_shift], label='Region 1 Firing rate after shift')
    # ax.plot(x, sig_freq1_norm[noise_shift:], label='Region 1 Frequency')
    # ax.plot(x, sig_fper2_norm[noise_shift:], label='Region 2 Firing rate')
    # ax.plot(x, sig_freq2_norm[noise_shift:], label='Region 2 Frequency')


    for arrow_x in [50, 170, 234, 330, 433]:
        # arrow_x = (200)
        arrow_y = sig_fper1_norm[int(arrow_x / dthist) + noise_shift]
        arrow_dx = noise_shift * dthist - 1
        arrow_dy = 0

        ax.arrow(arrow_x, arrow_y, arrow_dx, arrow_dy, head_width=0.015, head_length=5, length_includes_head=True,
                 fc='black')
    # ax.plot(x, sig_freq1_norm[noise_shift:], label='Region 1 Frequency before shift')
    # ax.plot(x, sig_freq1_norm[:-noise_shift], label='Region 1 Frequency')

    # ax.plot(x, sig_fper2_norm[:-noise_shift], label='Region 2 Firing rate')

    ax.legend(loc='upper right')
    ax.set_xlim(t_start, t_stop)
    ax.set_xlabel("Time t ($ms$)")

    ax.set_ylim(-0.1, 1.05)

    ax.set_yticks([])
    ax.set_yticklabels([])

    # ax.set_title("Noise and region signals after shift")

    fig.show()
    print(f"Frequency of the circuit: {run_frequency} Hz")

    plu.save_figure(fig, filename, runnumbers=[runnumber], l1=l1, l2=l2, run_frequency=run_frequency,
                    data_source=data_source)


def save_default():
    figure_problems_shifting_windows_noise_signal(data_source=data_source, filename=filename, runnumber=runnumber,
                                                  l1=l1, l2=l2, run_frequency=run_frequency)


if __name__ == "__main__":
    save_default()
