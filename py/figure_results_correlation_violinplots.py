import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matlab_utils as mlu
import settings as settings
import numpy as np
import pandas as pd

import plot_utils as plu

runnumbers_sett = settings.categories2['information_feedback_inhibitory_weak_brown_results_figures'][
    'runnumbers']  # Mixed noiseseed 46 and 80 [142] missing

analysis_info2_name = 'rhos_freq_noise1_reg2'
coherence_threshold = 0.9
compare_thresholds = [0, coherence_threshold]

figsize = (10, 3.4)

compare_signals_combinations = [['rhos_fper_noise2_reg2', 'rhos_freq_noise2_reg2'],
                                ['rhos_fper_noise2_reg1', 'rhos_freq_noise2_reg1'],
                                ['rhos_fper_noise1_reg1', 'rhos_freq_noise1_reg1'],
                                ['rhos_fper_noise1_reg2', 'rhos_freq_noise1_reg2']]
# compare_signals_combinations = []

filename_format_compare = 'figure_results_correlation_feedback_violinplot_compare_{compare_signal0}_vs_{compare_signal1}.png'
filename_format_thresholds = 'figure_results_correlation_feedback_violinplot_threshold_{analysis_info2_name}.png'


def figure_results_correlation_boxplots_compare_signals(runnumbers_sett, filename_format, compare_signals):
    """

    :param filename_format: Needs {compare_signal0} and {compare_signal1}!
    :param runnumbers_sett:
    :param compare_signals:
    :return:
    """
    corr_df2 = __figure_results_correlation_boxplots_prepare_df(runnumbers_sett)

    fig, ax = plt.subplots(ncols=2, sharey=True, figsize=figsize)

    for i, analysis_info2_name in enumerate(compare_signals):
        means = corr_df2.groupby(['feedback', 'Noiseseed'], as_index=False).mean()[analysis_info2_name]
        print(means)
        sns.violinplot(x='feedback', y=analysis_info2_name, hue='Noiseseed', split=True, data=corr_df2, ax=ax[i],
                       scale='count', inner='box', cut=0, linewidth=1.5)
        ax[i].set_ylabel('')
        ax[i].set_title(mlu.derive_analysis_info2_title(analysis_info2_name))
        ax[i].set_xlabel(r"Feedback $g_{{2 \to 1}}^{{e \to i}}$ in $mS/cm^2$")

    ax[0].set_ybound(None, 1.1)
    ax[0].set_ylabel('Correlation')
    ax[0].get_legend().remove()
    fig.show()

    if filename_format:
        filename = filename_format.format(compare_signal0=compare_signals[0], compare_signal1=compare_signals[1])
        plu.save_figure(fig, filename=filename, runnumbers=runnumbers_sett)


def figure_results_correlation_boxplots_compare_thresholds(runnumbers_sett, filename_format, analysis_info2_name,
                                                           compare_thresholds):
    """

    :param runnumbers_sett:
    :param filename_format: Needs {analysis_info2_name}!
    :param analysis_info2_name:
    :param compare_thresholds:
    :return:
    """

    corr_df2 = __figure_results_correlation_boxplots_prepare_df(runnumbers_sett)

    fig, ax = plt.subplots(ncols=2, sharey=True, figsize=figsize)

    for i, threshold in enumerate(compare_thresholds):
        sns.violinplot(x='feedback', y=analysis_info2_name, hue='Noiseseed', split=True,
                       data=corr_df2[corr_df2['coh'] >= threshold], ax=ax[i],
                       scale='count', inner='box', cut=0, linewidth=1.5)
        if threshold == 0:
            ax[i].set_title("All conditions")
            pass
        else:
            ax[i].set_title(f"Threshold $\geq$ {threshold}")
            pass
        ax[i].set_xlabel(r"Feedback $g_{{2 \to 1}}^{{e \to i}}$ in $mS/cm^2$")

    # fig.suptitle(mlu.derive_analysis_info2_title(analysis_info2_name))

    ax[0].set_ybound(None, 1)
    ax[0].set_ylabel('Correlation')
    ax[0].get_legend().remove()
    fig.show()

    if filename_format:
        filename = filename_format.format(analysis_info2_name=analysis_info2_name)
        plu.save_figure(fig, filename=filename, runnumbers=runnumbers_sett)


def __figure_results_correlation_boxplots_prepare_df(runnumbers_sett):
    noisetypes = {1: "White", 2: "Brown", 3: "Pink"}

    corr_df2 = pd.DataFrame()

    for runnumbers in runnumbers_sett:
        for runnumber in runnumbers:
            sett = mlu.get_clean_settings(runnumber)['sett']
            feedback_conductance_ee = sett['g_syn_ee_r'][0, 1]
            feedback_conductance_ei = sett['g_syn_ei_r'][0, 1]
            noisetype = noisetypes[sett['noisetype']]
            noiseamp = sett['noiseamp']

            analysis_standard2_df = mlu.run_analysis_standard2_to_df(runnumber)

            correlations = mlu.get_max_correlations(runnumber)

            new = pd.DataFrame(
                {'feedback': feedback_conductance_ei, 'coh': analysis_standard2_df['coh'],
                 'correlation': correlations[analysis_info2_name],
                 'threshold': list(analysis_standard2_df['coh'] >= coherence_threshold), 'Noiseseed': sett['noiseseed'],
                 'noisetype': noisetype,
                 'noiseamp': noiseamp})
            for col in correlations.columns:
                new[col] = correlations[col]

            corr_df2 = corr_df2.append(new)
    return corr_df2


def save_default():
    for compare_signals in compare_signals_combinations:
        figure_results_correlation_boxplots_compare_signals(compare_signals=compare_signals,
                                                            runnumbers_sett=runnumbers_sett,
                                                            filename_format=filename_format_compare)
    figure_results_correlation_boxplots_compare_thresholds(runnumbers_sett=runnumbers_sett,
                                                           analysis_info2_name=analysis_info2_name,
                                                           compare_thresholds=compare_thresholds,
                                                           filename_format=filename_format_thresholds)


if __name__ == "__main__":
    save_default()
