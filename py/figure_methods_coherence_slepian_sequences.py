# Code from http://thomas-cokelaer.info/software/spectrum/html/user/ref_mtm.html

import spectrum
import seaborn as sns
import matplotlib.pyplot as plt

import plot_utils as plu


def methods_coherence_slepian_sequences(T, TW, filename=None):
    # Generate the slepian sequences, here using the time-halfbandwith-product
    [w, eigens] = spectrum.dpss(T, TW / 2, 4)

    # fig, ax = plt.subplots(figsize=(8, 5))
    fig, ax = plt.subplots(figsize=(6, 4.4))
    # ax.canvas(200, 350)

    sns.lineplot(data=w, ax=ax)

    ax.set_xlim([100, 900])
    ax.set_xlabel(r"Time t in $ms$")

    ax.set_ylim([-0.12, 0.12])

    ax.legend(['1st sequence', '2nd sequence', '3rd sequence', '4th sequence'])
    # ax.set_title(f"Slepian sequences for T={T}, TW={TW}")

    fig.show()

    plu.save_figure(fig, filename, T=T, TW=TW)


def save_default():
    methods_coherence_slepian_sequences(T=1000, TW=30, filename='figure_methods_coherence_slepian_sequences.png')


if __name__ == "__main__":
    save_default()
