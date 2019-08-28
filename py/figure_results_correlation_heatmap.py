import matplotlib
# matplotlib.use('Qt5')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matlab_utils as mlu
import settings as settings
import numpy as np
import pandas as pd

import plot_utils as plu

# runnumbers_sett = [[126], [128], [129], [132], [133]]  # Weak Brown
# runnumbers_sett = [[117, 125], [124], [118], [122]]  # Strong brown
# runnumbers_sett = [[112, 115], [114], [113], [116]]  # Pink
runnumbers_sett = settings.categories2['information_feedback_inhibitory_weak_brown_results_figures'][
    'runnumbers']  # Mixed noiseseed 46 and 80 [142] missing

signal_type = 'fper'  # 'fper' or 'freq' (or 'power')
signal_from = 'noise'  # 'noise' or 'reg'
region_from = 1
region_to = 2

coherence_threshold = 0.00

analysis_info2_name = f'rhos_{signal_type}_{signal_from}{region_from}_reg{region_to}'
analysis_info2_names = ['rhos_fper_noise1_reg1', 'rhos_fper_noise1_reg2', 'rhos_freq_noise1_reg1',
                        'rhos_freq_noise1_reg2']
analysis_info2_names = ['rhos_fper_noise1_reg1', 'rhos_fper_noise1_reg2']
analysis_info2_names = ['rhos_freq_noise1_reg1', 'rhos_freq_noise1_reg2']

filename_format = 'figure_results_correlation_heatmap_ee{feedback_conductance_ee}_ei{feedback_conductance_ei}_{analysis_info2_name}_coh{coherence_threshold}.png'

fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(10, 5.2))
corr_df2 = pd.DataFrame()


def figure_results_correlation_heatmap(runnumbers, analysis_info2_name, coherence_threshold, filename_format,
                                       debug=False, show_info_fb_inh=True):
    analysis_info2_title = mlu.derive_analysis_info2_title(analysis_info2_name)

    sett = mlu.get_clean_settings(runnumbers[0])['sett']
    feedback_conductance_ee = sett['g_syn_ee_r'][0, 1]
    feedback_conductance_ei = sett['g_syn_ei_r'][0, 1]
    noise_title = mlu.get_noise_title(sett['noiseamp'], sett['noisetype'])

    analysis_standard2_df = mlu.run_analysis_standard2_to_df(runnumbers[0])
    coherences_all = [mlu.run_analysis_standard2_to_df(runnumber) for runnumber in runnumbers]
    coherences = pd.concat(coherences_all).groupby(level=[0, 1]).mean()['coh']

    # print(analysis_standard2_df[analysis_standard2_df['coh'] >= coherence_threshold])

    correlations_all = [mlu.get_max_correlations(runnumber) for runnumber in runnumbers]
    correlations = pd.concat(correlations_all).groupby(level=[0, 1]).mean()
    correlations = correlations[analysis_info2_name]

    correlations[coherences < coherence_threshold] = np.nan

    print(
        f"{analysis_info2_name}, feedback {feedback_conductance_ei} mS/cm^2. Correlation limits (min, max): ({correlations.min()},{correlations.max()})")

    fig, ax = plt.subplots()

    sns.heatmap(correlations.unstack().transpose(), cmap='coolwarm', vmin=-0.3, vmax=1, center=0, ax=ax)
    ax.invert_yaxis()

    plu.set_heatmap_axes(ax)

    # Insert a textbox listing the feedback conductance
    text = mlu.get_infobox_text(feedback_conductance_ee=feedback_conductance_ee, feedback_conductance_ei=feedback_conductance_ei, runnumbers=runnumbers, debug=debug, show_info_fb_inh=True)

    plu.set_textbox(ax, text, loc='lower right')

    # ax.set_title(f"{analysis_info2_title}")

    ax.legend(loc='lower right')

    fig.show()

    if filename_format:
        # Convert the float into a string. We are always <1, so cut off everything in front of decimal
        feedback_conductance_ee_str = "{:4.3f}".format(feedback_conductance_ee).replace(".", "_")[2:]
        feedback_conductance_ei_str = "{:4.3f}".format(feedback_conductance_ei).replace(".", "_")[2:]
        coherence_threshold_str = "{:3.2f}".format(coherence_threshold).replace('.', "")

        filename = filename_format.format(analysis_info2_name=analysis_info2_name,
                                          feedback_conductance_ee=feedback_conductance_ee_str,
                                          feedback_conductance_ei=feedback_conductance_ei_str,
                                          coherence_threshold=coherence_threshold_str)

        plu.save_figure(fig, filename, runnumbers=runnumbers,
                        feedback_conductance_ee=feedback_conductance_ee,
                        feedback_conductance_ei=feedback_conductance_ei,
                        analysis_info2_name=analysis_info2_name,
                        coherence_threshold=coherence_threshold)


def save_default():
    coherence_threshold = 0
    analysis_info2_names = ['rhos_fper_noise1_reg2', 'rhos_freq_noise1_reg1', 'rhos_freq_noise1_reg2']
    for analysis_info2_name in analysis_info2_names:
        for runnumbers in runnumbers_sett:
            figure_results_correlation_heatmap(runnumbers=runnumbers, analysis_info2_name=analysis_info2_name,
                                               coherence_threshold=coherence_threshold, filename_format=filename_format)


if __name__ == "__main__":
    save_default()