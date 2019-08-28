import os
import numpy as np
import pandas as pd
import scipy.signal

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context("paper", font_scale=1.4)

sns.axes_style("whitegrid", rc={"font.size": 15, "axes.titlesize": 25, "axes.labelsize": 15, "xtick.labelsize": 15,
                                "ytick.labelsize": 15})

import matlab_utils as mlu
import settings as settings


def set_heatmap_axes(ax):
    # x-axis
    num_xticks = 9

    xlabel = '$I_{inj}^{i}$ to region 1 ($\\mu A/cm^2$)'
    xticks = np.linspace(0.5, 39.5, num=num_xticks)
    xticklabels = np.linspace(0.4, 2.0, num=num_xticks).round(decimals=1)

    ax.set_xlabel(xlabel)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=0)

    # y-axis
    num_yticks = 4

    y_max = ax.get_ylim()[1]  # We need the maximum value of y to adjust the range of our yticks

    ylabel = f"Total synaptic conductance $g_{{1 \\rightarrow 2}}^{{e \\to e, i}}$ ($mS/cm^2$)"
    yticks = np.linspace(0.5, y_max-0.5, num=num_yticks)
    yticklabels = np.linspace(0, 0.3, num=num_yticks)

    ax.set_ylabel(ylabel)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels, rotation=0)
    ax.tick_params('both', length=2, width=1, which='major')

    return ax


def set_textbox(ax, text, loc=None):
    if loc is None:
        loc = 'upper left'

    if 'upper' in loc:
        y = 0.97
        verticalalignment = 'top'
    elif 'lower' in loc:
        y = 0.03
        verticalalignment = 'bottom'

    if 'left' in loc:
        x = 0.03
        horizontalalignment = 'left'
    elif 'right' in loc:
        x = 0.97
        horizontalalignment = 'right'


    props = dict(boxstyle='round', facecolor='white', alpha=0.5, edgecolor='grey')
    ax.text(x, y, transform=ax.transAxes,
            verticalalignment=verticalalignment, s=text, bbox=props, horizontalalignment=horizontalalignment)

    return ax


def save_figure(fig, filename, runnumbers=None, **kwargs):
    if filename is not None:
        figures_path = settings.figures_save_to
        filepath = os.path.join(figures_path, filename)

        fig.savefig(filepath, bbox_inches='tight')
        print(f"Saved figure to {filepath}")

        __save_figure_summary(filename, runnumbers, **kwargs)


def __save_figure_summary(filename, runnumbers, **kwargs):
    summary_buffer = f"#### {filename} ####\n"
    summary_buffer += f"runnumbers: {runnumbers}\n" if runnumbers else ""
    summary_buffer += f"{kwargs}\n" if kwargs else ""
    summary_buffer += "\n"
    with open(settings.figures_summary_file, "a+") as fig_summary_fp:
        fig_summary_fp.write(summary_buffer)


def plot_spiketrains_scatter_region(runnumber, l1, l2, region, savefigure=True):
    sett = mlu.get_clean_settings(runnumber)['sett']
    spikes_excitatory, spikes_inhibitory = mlu.get_spiketrains_df(runnumber, l1, l2)

    spikes_excitatory['neuron_idx'] = spikes_excitatory['neuron_idx'] + sett['Ni']

    fig, ax = plt.subplots(figsize=(20, 7.5))

    sns.scatterplot(x='t', y='neuron_idx', color='blue', s=5,
                    data=spikes_excitatory[spikes_excitatory['region'] == region], ax=ax, label='Pyramidal Cells')
    sns.scatterplot(x='t', y='neuron_idx', color='red', s=5,
                    data=spikes_inhibitory[spikes_inhibitory['region'] == region], ax=ax, label='Interneurons')

    ax.set_ylabel('Neuron index')
    ax.set_xlabel('Time ($s$)')
    ax.legend(loc='upper right')

    fig.show()

    if savefigure:
        name = f'run{runnumber}_l1{l1}_l2{l2}_region{region}_spiketrains.png'
        fig.savefig(os.path.join(settings.run_figures_dir(runnumber), name), bbox_inches='tight', pad_inches=0)

    return fig


def plot_spiketrains_scatter(runnumber, l1, l2, savefigure=True, regions=None):
    sett = mlu.get_clean_settings(runnumber)['sett']
    spikes_excitatory, spikes_inhibitory = mlu.get_spiketrains_df(runnumber, l1, l2)

    if regions is None:
        regions = sorted(spikes_excitatory.region.unique().astype(int))

    spikes_excitatory['neuron_idx'] = spikes_excitatory['neuron_idx'] + sett['Ni']

    fig, axes = plt.subplots(nrows=len(regions), sharex=False, figsize=(40, 15))

    for region, ax in zip(regions, axes):
        sns.scatterplot(x='t', y='neuron_idx', color='red', s=5,
                        data=spikes_inhibitory[spikes_inhibitory['region'] == region], ax=ax)
        sns.scatterplot(x='t', y='neuron_idx', color='blue', s=5,
                        data=spikes_excitatory[spikes_excitatory['region'] == region], ax=ax)

    fig.show()

    if savefigure:
        name = f'run{runnumber}_l1{l1}_l2{l2}_spiketrains.png'
        fig.savefig(os.path.join(settings.run_figures_dir(runnumber), name), bbox_inches='tight', pad_inches=0)

    return fig


def plot_spiketrain_histogram(runnumber, l1, l2, savefigure=True, findpeaks=True, cwt_widths=np.arange(4, 25)):
    sett = mlu.get_clean_settings(runnumber)['sett']
    spikes_excitatory, spikes_inhibitory = mlu.get_spiketrains_df(runnumber, l1, l2)

    bins = np.linspace(start=0, stop=sett['Ttot'], num=int(sett['Ttot'] / sett['dthist'] + 1), endpoint=True)

    region1_excitatory_spikes_binned, _ = np.histogram(spikes_excitatory[spikes_excitatory['region'] == 1]['t'],
                                                       bins=bins)
    region2_excitatory_spikes_binned, _ = np.histogram(spikes_excitatory[spikes_excitatory['region'] == 2]['t'],
                                                       bins=bins)

    fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(40, 15))

    ax[0].bar(x=bins[:-1], height=region1_excitatory_spikes_binned[:])
    ax[1].bar(x=bins[:-1], height=region2_excitatory_spikes_binned[:])

    ax[1].invert_yaxis()

    if findpeaks:
        region1_peaks = scipy.signal.find_peaks_cwt(region1_excitatory_spikes_binned, widths=cwt_widths)
        region2_peaks = scipy.signal.find_peaks_cwt(region2_excitatory_spikes_binned, widths=cwt_widths)

        ax[0].vlines(region1_peaks * sett['dthist'], 0, 10, colors='k')
        ax[1].vlines(region2_peaks * sett['dthist'], 0, 10, colors='k')

    fig.subplots_adjust(wspace=0, hspace=0)

    ax[0].set_title(
        f"Run {runnumber}, loop1={l1}, loop2={l2} - $reg_1$ (upper) and $reg_2$ (lower) excitatory cell spike histograms")

    fig.show()

    if savefigure:
        name = 'run{}_l1{}_l2{}_excitatory_histograms.png'.format(runnumber, l1, l2)
        fig.savefig(os.path.join(settings.run_figures_dir(runnumber), name), bbox_inches='tight', pad_inches=0)

    return fig


### Maybe for later:
# def plot_run_analysis2_heatmap_generic(runnumber, heatmap_dataframe, plot_title, vmin=0, vmax=1, savefig=True, savepath=None):
#     run_settings_loops = mlu.get_run_loops(runnumber)
#     sett = mlu.get_clean_settings(runnumber)['sett']
#
#
#     pass


def plot_run_analysis_standard2_heatmap(runnumber, analysis_name='coh', savefigure=True):
    """
    Plots a heatmap of coherence for given runnumber. Even though we can give other analysis_names,
    it probably doesn't generalize very well because of sns.heatmap(..., vmin=0, vmax=1, ...)
    :param runnumber:
    :param analysis_name:
    :param savefig:
    :return: fig
    """
    run_analysis_standard2_df = mlu.run_analysis_standard2_to_df(runnumber)
    run_settings_loops = mlu.get_run_loops(runnumber)
    sett = mlu.get_clean_settings(runnumber)['sett']

    if run_settings_loops[2]['name'] == 'g_syn_loop':
        region_from = run_settings_loops[2]['region_from']
        region_to = run_settings_loops[2]['region_to']
        fixed_conductance_ee = sett['g_syn_ee_r'][region_from, region_to]
        fixed_conductance_ei = sett['g_syn_ei_r'][region_from, region_to]

    analysis_df = run_analysis_standard2_df[analysis_name].unstack().transpose()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    sns.heatmap(analysis_df, vmin=0, vmax=1, cmap='inferno', ax=ax)

    # x-axis
    ax.set_xlabel(run_settings_loops[1]['name_readable'])
    label_idxs = range(0, len(run_settings_loops[1]['values_inhibitory']), 3)
    ax.set_xticks(label_idxs)
    ax.set_xticklabels(np.around(run_settings_loops[1]['values_inhibitory'][ax.get_xticks().astype(int)], decimals=2))

    # y-axis
    ax.invert_yaxis()
    ax.set_ylabel(run_settings_loops[2]['name_readable'])
    ylabels = run_settings_loops[2]['values']
    ax.set_yticks(range(0, len(ylabels), 2))
    ax.set_yticklabels(ylabels[ax.get_yticks()], rotation=0)

    # The rest
    ax.set_title(f'Run{runnumber} - {mlu.analysis_standard2_names[analysis_name]}')

    plt.show()

    if savefigure:
        name = f'run{runnumber}_{analysis_name}.png'
        fig.savefig(os.path.join(settings.run_figures_dir(runnumber), name), bbox_inches='tight', pad_inches=0)
    return fig


#
# def plot_run_analysis(runnumber, plot_analysis_names=['coh']):
#     run_analysis2_df = mlu.run_analysis_standard2_to_df(runnumber)
#     run_settings_loops = mlu.get_run_loops(runnumber)
#     sett = mlu.get_clean_settings(runnumber)['sett']
#
#     title_suffix = ''
#     if run_settings_loops[2]['name'] == 'g_syn_loop':
#         feedforward = (0, 1)
#         region_from = run_settings_loops[2]['region_from']
#         region_to = run_settings_loops[2]['region_to']
#         title_suffix = r', total synaptic conductance $reg_{} \rightarrow reg_{}$ ${}$ $mS/cm^2$'.format(region_to,
#                                                                                                          region_from,
#                                                                                                          sett[
#                                                                                                              'g_syn_ei_r'][
#                                                                                                              region_from, region_to])
#
#     for analysis2_name in plot_analysis_names:
#         dataframe = run_analysis2_df[analysis2_name].unstack().transpose()
#
#         ax = sns.heatmap(dataframe, vmin=0, vmax=1, cmap='inferno')
#
#         # x-axis
#         ax.set_xlabel(run_settings_loops[1]['name_readable'])
#         label_idxs = np.arange(0, len(run_settings_loops[1]['values_inhibitory']) - 1, 3)
#         ax.set_xticks(label_idxs)
#         ax.set_xticklabels(np.around(run_settings_loops[1]['values_inhibitory'][label_idxs], decimals=2))
#
#         # y-axis
#         ax.invert_yaxis()
#         ax.set_ylabel(run_settings_loops[2]['name_readable'])
#         ylabels = run_settings_loops[2]['values']
#         ax.set_yticks(range(0, len(ylabels), 2))
#         ax.set_yticklabels(ylabels[ax.get_yticks()], rotation=0)
#
#         # The rest
#         ax.set_title('Run{} - '.format(runnumber) + mlu.analysis_standard2_names[analysis2_name] + title_suffix)
#         # plt.show()
#         plt.show()
#         return ax.get_figure()


def plot_coherence_frequencies(runnumber, l2, savefigure=True):
    """
    As we have a fixed synaptic conductance but varying injected current, we have only l2 given here
    :param runnumber:
    :param l2: Fixed l2-value for the analysis. Attention!: matlab-counting, starting with 1!
    :return:
    """

    # Load all the settings and analyses needed
    run_settings_loops = mlu.get_run_loops(runnumber)
    analysis_standard_reg1_df, analysis_standard_reg2_df = mlu.run_analysis_standard_to_df(runnumber)
    analysis_standard2_df = mlu.run_analysis_standard2_to_df(runnumber)
    analysis_coherences_frequency = mlu.loadmat(settings.run_analysis_coherencefrequency_filepath(runnumber))[
        'coherences']

    l1steps, l2steps = analysis_coherences_frequency.shape

    # Check if matlab-counting holds. Lowest l2 can be 1, highest can be the number of elements.
    assert (l2 >= 1 and l2 <= l2steps)

    df_coherences_frequency = pd.DataFrame(
        [coherences.coh_exc for coherences in analysis_coherences_frequency[:, l2 - 1]]).transpose()

    avgmorfreqs1 = analysis_standard_reg1_df['avgmorfreq'][:, l2 - 1]
    avgmorfreqs2 = analysis_standard_reg2_df['avgmorfreq'][:, l2 - 1]

    ### Plotting
    fixed_synaptic_conductance = run_settings_loops[2]['values'][l2 - 1]

    yaxis_frequencies = analysis_coherences_frequency[1, l2 - 1].f_exc.round(2)

    # Adding an offset to move the dots into the middle of each bin
    frequency_indices1 = [np.argmin(np.abs(yaxis_frequencies - avgmorfreq)) for avgmorfreq in avgmorfreqs1]
    frequency_indices2 = [np.argmin(np.abs(yaxis_frequencies - avgmorfreq)) for avgmorfreq in avgmorfreqs2]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    sns.heatmap(data=df_coherences_frequency, vmin=0, vmax=1, cmap='inferno', ax=ax)

    ax.scatter(np.arange(l1steps) + 0.5, frequency_indices1, color='blue', marker="+", label="Frequency Region 1")
    ax.scatter(np.arange(l1steps) + 0.5, frequency_indices2, color='green', marker="o", label="Frequency Region 2",
               alpha=0.5)
    ax.legend()

    # ax.scatter(index, frequency_indices2[index], color='blue', marker="x")
    # np.min(np.abs(np.subtract(avgmorfreqs, df_coherences_frequency, 2)))

    # x-axis
    ax.set_xlabel(run_settings_loops[1]['name_readable'])
    ax.set_xticks(range(0, len(run_settings_loops[1]['values']), 4))
    ax.set_xticklabels(np.around(run_settings_loops[1]['values'][ax.get_xticks().astype(int)], decimals=2))

    # y-axis
    ax.invert_yaxis()
    ax.set_ylabel('Frequency')
    ax.set_yticklabels(yaxis_frequencies[ax.get_yticks().astype(int)], rotation=0)

    # The rest
    ax.set_title(
        f'Run{runnumber}, Coherence (feedforward conductance ${fixed_synaptic_conductance} mS/cm^2$)')

    plt.show()

    if savefigure:
        fig.savefig(os.path.join(settings.run_figures_dir(runnumber), f'run{runnumber}_l2{l2}_coherence_frequency.png'))

    return fig
