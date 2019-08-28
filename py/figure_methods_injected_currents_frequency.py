import os
import numpy as np
import matplotlib.pyplot as plt
import plot_utils as plu
import seaborn as sns

import matlab_utils as mlu
import settings as settings

sns.set_context("paper", font_scale=1.4)


def figure_methods_injected_currents_frequency(runnumber, l2, filename_currents=None, filename_frequency=None):
    ### Define injected currents
    num = 40
    i_inh = np.linspace(0.4, 2.0, num)
    i_exc = 0.4652 * i_inh ** 4 - 1.9860 * i_inh ** 3 + 3.2879 * i_inh ** 2 - 1.0623 * i_inh + 0.7546

    xaxis = range(1, 41)
    ### Plot curves of injected currents:
    fig_currents, ax = plt.subplots()
    sns.lineplot(xaxis, i_exc, ax=ax, label=r'$I_{inj}^{exc}$', color='red')
    sns.lineplot(xaxis, i_inh, ax=ax, label=r'$I_{inj}^{inh}$', color='blue')

    ax.set_ylabel('Injected current (${\mu A / cm^2}$)')
    ax.set_xlabel("Index of injected currents")

    # ax.set_title("Injected currents $I_{inj}^{inh}$ and $I_{inj}^{exc}$")
    fig_currents.show()

    plu.save_figure(fig_currents, filename_currents, runnumbers=[runnumber], l2=l2)

    # if savefigures:
    #     fig_currents.savefig(os.path.join(settings.py_figures_dir, f'figure_injected_currents_exc_inh.png'), bbox_inches='tight', pad_inches=0.1)

    ### Get frequency and PPC curve of runnumber
    analysis_standard_df_reg1, analysis_standard_df_reg2 = mlu.run_analysis_standard_to_df(runnumber=runnumber)
    freqe = analysis_standard_df_reg1['freqe'].loc[:, l2]
    avgmorfreq = analysis_standard_df_reg1['avgmorfreq'].loc[:, l2]
    phaselocke = analysis_standard_df_reg1['Phaselocke'].loc[:, l2]

    ### Plot curves of frequency and PPC (Phaselock)
    fig_frequency, ax_freq = plt.subplots()

    ax_phaselock = ax_freq.twinx()
    # ax_phaselock.axhline(y=0.1, color='black', alpha=0.9, linestyle='--')  # Threshold line for extremely low PPC (i.e., no real oscillations)
    sns.lineplot(y=phaselocke, x=xaxis, ax=ax_phaselock, label='PPC value', color='black')

    ax_phaselock.set_ylim([0, 0.8])
    ax_phaselock.set_ylabel("PPC value")

    sns.lineplot(y=avgmorfreq, x=xaxis, ax=ax_freq, label='Frequency (Morlet)')
    sns.lineplot(y=freqe, x=xaxis, ax=ax_freq, label='Frequency (Autocorrelation)')

    # ax_freq.set_xticklabels(np.linspace(1, 40, 41))
    ax_freq.set_xlim(left=0, right=41)
    ax_freq.set_xlabel("Index of injected currents")
    ax_freq.set_ylim([35, 75])
    ax_freq.set_ylabel("Frequency (Hz)")

    ax_freq.legend(loc='upper left')
    # ax_freq.set_title("Intrinsic frequency and PPC")

    fig_frequency.show()

    plu.save_figure(fig_frequency, filename_frequency, runnumbers=[runnumber], l2=l2)


def save_default():
    figure_methods_injected_currents_frequency(runnumber=81, l2=0,
                                               filename_currents='figure_methods_injected_currents_exc_inh.png',
                                               filename_frequency='figure_methods_injected_currents_frequency_ppc.png'
                                               )


if __name__ == "__main__":
    save_default()
