import os
import numpy as np
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
import seaborn as sns
from matplotlib.lines import Line2D

import matlab_utils as mlu
import plot_utils as plu
import settings as settings


def methods_analysis_spikes_scatterplot(runnumber, l1, l2, region, start, stop, filename=None):
    sett = mlu.get_clean_settings(runnumber)['sett']
    spikes_excitatory, spikes_inhibitory = mlu.get_spiketrains_df(runnumber, l1, l2)

    spikes_excitatory['neuron_idx'] = spikes_excitatory['neuron_idx'] + sett['Ni']

    # Filter for region
    spikes_excitatory = spikes_excitatory[spikes_excitatory['region'] == region]
    spikes_inhibitory = spikes_inhibitory[spikes_inhibitory['region'] == region]

    # Filter for start <= t <= end
    spikes_excitatory = spikes_excitatory[spikes_excitatory['t'] >= start]
    spikes_excitatory = spikes_excitatory[spikes_excitatory['t'] <= stop]

    spikes_inhibitory = spikes_inhibitory[spikes_inhibitory['t'] >= start]
    spikes_inhibitory = spikes_inhibitory[spikes_inhibitory['t'] <= stop]

    # Plot spikes in scatterplot
    fig, ax = plt.subplots(figsize=(10, 4))

    sns.scatterplot(x='t', y='neuron_idx', color='red', s=6,
                    data=spikes_excitatory, ax=ax, label='Pyramidal Cells')
    sns.scatterplot(x='t', y='neuron_idx', color='blue', s=6,
                    data=spikes_inhibitory, ax=ax, label='Interneurons')
    ax.set_ylim(ymin=-20)
    ax.set_ylabel('Neuron index')
    ax.set_xlabel('Time t ($ms$)')
    ax.legend(loc='upper left')

    # ax.set_title('Pyramidal cell (red) and interneuron (blue) spiketrains')

    # Create dummy Line2D objects for legend
    h1 = Line2D([0], [0], marker='o', markersize=np.sqrt(30), color='red', linestyle='None')
    h2 = Line2D([0], [0], marker='o', markersize=np.sqrt(30), color='blue', linestyle='None')

    ax.legend([h1, h2], ['Pyramidal cells', 'Interneurons'], loc='upper right')

    fig.show()

    ppc_value = mlu.run_analysis_standard_to_df(runnumber)[region-1]['Phaselocke'][l1-1, l2-1]
    print('ppc_value: ', ppc_value)

    plu.save_figure(fig, filename, runnumbers=[runnumber], l1=l1, l2=l2, region=region, start=start, stop=stop, ppc_value=ppc_value)


def methods_analysis_spike_density_histogram(runnumber, l1, l2, region, start, stop, filename=None):
    sett = mlu.get_clean_settings(runnumber)['sett']
    spikes_excitatory, spikes_inhibitory = mlu.get_spiketrains_df(runnumber, l1, l2)

    spikes_excitatory['neuron_idx'] = spikes_excitatory['neuron_idx'] + sett['Ni']

    # Filter for region
    spikes_excitatory = spikes_excitatory[spikes_excitatory['region'] == region]
    spikes_inhibitory = spikes_inhibitory[spikes_inhibitory['region'] == region]

    # Filter for start <= t <= end
    spikes_excitatory = spikes_excitatory[spikes_excitatory['t'] >= start]
    spikes_excitatory = spikes_excitatory[spikes_excitatory['t'] <= stop]

    spikes_inhibitory = spikes_inhibitory[spikes_inhibitory['t'] >= start]
    spikes_inhibitory = spikes_inhibitory[spikes_inhibitory['t'] <= stop]

    # Bin the spikes for histograms
    bins = np.linspace(start=start, stop=stop, num=int((stop - start) / sett['dthist'] + 1), endpoint=True)
    excitatory_spikes_binned, _ = np.histogram(spikes_excitatory['t'], bins=bins)
    inhibitory_spikes_binned, _ = np.histogram(spikes_inhibitory['t'], bins=bins)

    excitatory_spikes_density = 1000 * 1 / (sett['dthist'] * sett['Ne']) * excitatory_spikes_binned
    inhibitory_spikes_density = 1000 * 1 / (sett['dthist'] * sett['Ni']) * inhibitory_spikes_binned

    fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 4.5))

    ax[0].bar(x=bins[:-1], height=excitatory_spikes_density, color='red', label='Pyramidal cells')
    ax[1].bar(x=bins[:-1], height=inhibitory_spikes_density, color='blue', label='Interneurons')

    handles = [mpatches.Patch(color='red', label='Pyramidal cells'), mpatches.Patch(color='blue', label='Interneurons')]

    ax[0].legend(handles=handles, loc='upper right')

    ax[1].invert_yaxis()
    fig.subplots_adjust(wspace=0, hspace=0)

    ax[1].set_xlabel('Time t ($ms$)')
    ax[0].set_ylabel('Spikes/s')
    ax[1].set_ylabel('Spikes/s')


    # ax[0].set_title(
    #     f"Pyramidal cell (upper) and interneuron (lower) spike density plots")

    fig.show()

    ppc_value = mlu.run_analysis_standard_to_df(runnumber)[region - 1]['Phaselocke'][l1 - 1, l2 - 1]

    plu.save_figure(fig, filename, runnumbers=[runnumber], l1=l1, l2=l2, region=region, start=start, stop=stop, ppc_value=ppc_value)



def save_default():
    methods_analysis_spikes_scatterplot(runnumber=52, l1=2, l2=1, region=1, start=0, stop=600,
                                             filename='figure_appendix_low_ppc_spiketrains.png')
    methods_analysis_spikes_scatterplot(runnumber=52, l1=25, l2=1, region=1, start=0, stop=600,
                                             filename='figure_appendix_high_ppc_spiketrains.png')
    methods_analysis_spike_density_histogram(runnumber=52, l1=25, l2=1, region=1, start=0, stop=600,
                                             filename='figure_methods_high_ppc_histogram.png')


if __name__ == "__main__":
    save_default()
