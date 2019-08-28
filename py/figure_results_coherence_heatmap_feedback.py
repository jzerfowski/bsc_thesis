import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt
import seaborn as sns

import matlab_utils as mlu
import settings as settings
import plot_utils as plu

filename_format = 'figure_results_coherence_heatmap_feedback_ee{feedback_conductance_ee}_ei{feedback_conductance_ei}.png'
# filename_format = None



# After changing this we should also rerun figure_appendix_analysis_standard_heatmap_with_feedback!
# runnumbers_sett = [[126], [128], [129], [132], [133]]  # Weak Brown
# runnumbers_sett = settings.categories2['information_feedback_inhibitory_weak_brown_results_figures']['runnumbers']  # Mixed noiseseed 46 and 80 [142] missing
# runnumbers_sett = settings.categories2['fixed_feedback_excitatory_inhibitory']['runnumbers']  # Coherence for conditions with both feedback types


runnumbers_sett = [[81, 107, 108], [127], [106, 104], [130], [105]]  # Valid entries of fixed_feedback_inhibitory
runnumbers_sett = [81, 107, 108], [127, 154], [106, 104, 152], [130, 151], [105, 155]

coherence_threshold = 0.9




def figure_results_coherence_heatmap_with_feedback(runnumbers, filename_format, show_info_fb_inh=True, debug=False):
    """
    :param runnumbers: All runnumbers need to have the same settings except seed!
    :param filename: needs {feedback_conductance_ee} and {feedback_conductance_ei}
    :return:
    """
    sett = mlu.get_clean_settings(runnumbers[0])['sett']
    feedback_conductance_ee = sett['g_syn_ee_r'][0, 1]
    feedback_conductance_ei = sett['g_syn_ei_r'][0, 1]


    # Compute the mean over all runnumbers for standard2 analysis
    analyses_standard2_dfs = [mlu.run_analysis_standard2_to_df(runnumber) for runnumber in runnumbers]
    analysis_standard2_mean = pd.concat(analyses_standard2_dfs).groupby(level=[0, 1]).mean()

    coherence_mean = analysis_standard2_mean['coh']

    print(f"Runs {runnumbers} coherence >= {coherence_threshold}: {sum(coherence_mean >= coherence_threshold)}")

    ## Plotting coherence
    fig, ax = plt.subplots()

    sns.heatmap(coherence_mean.unstack().transpose(), cmap='inferno', ax=ax, vmin=0, vmax=1)
    ax.invert_yaxis()

    plu.set_heatmap_axes(ax)

    # ax.set_title(f'Coherence - pyramidal neurons')

    # Insert a textbox listing the feedback conductance
    text = mlu.get_infobox_text(feedback_conductance_ee=feedback_conductance_ee, feedback_conductance_ei=feedback_conductance_ei, debug=debug, show_info_fb_inh=show_info_fb_inh)

    plu.set_textbox(ax, text)

    fig.show()

    if filename_format:
        # Convert the float into a string. We are always <1, so cut off everything in front of decimal
        feedback_conductance_ee_str = "{:4.3f}".format(feedback_conductance_ee).replace(".", "_")[2:]
        feedback_conductance_ei_str = "{:4.3f}".format(feedback_conductance_ei).replace(".", "_")[2:]

        filename = filename_format.format(feedback_conductance_ee=feedback_conductance_ee_str,
                                          feedback_conductance_ei=feedback_conductance_ei_str)

        plu.save_figure(fig, filename, runnumbers=runnumbers,
                        feedback_conductance_ee=feedback_conductance_ee,
                        feedback_conductance_ei=feedback_conductance_ei)


def save_default():
    for runnumbers in runnumbers_sett:
        figure_results_coherence_heatmap_with_feedback(runnumbers, filename_format=filename_format, debug=False)



if __name__ == "__main__":
    # filename_format = None
    save_default()
