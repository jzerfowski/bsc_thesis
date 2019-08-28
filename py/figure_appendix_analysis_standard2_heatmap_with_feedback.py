import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt
import seaborn as sns

import matlab_utils as mlu
import settings as settings
import plot_utils as plu

# filename_format = 'figure_appendix_heatmap_{analysis_standard_name}_reg{region}_ee{feedback_conductance_ee}_ei{feedback_conductance_ei}.png'

from figure_results_coherence_heatmap_feedback import runnumbers_sett

def figure_appendix_analysis_standard_heatmap_with_feedback(runnumbers, analysis_standard2_name, filename_format,
                                                            debug=False):
    """
    :param runnumbers: All runnumbers need to have the same settings except seed!
    :param filename: needs {analysis_standard_name} {feedback_conductance_ee} and {feedback_conductance_ei} and {region}
    :return:
    """

    sett = mlu.get_clean_settings(runnumbers[0])['sett']
    feedback_conductance_ee = sett['g_syn_ee_r'][0, 1]
    feedback_conductance_ei = sett['g_syn_ei_r'][0, 1]

    # Compute the means for standard analyses
    analyses_standard = {}

    group_analyses_standard2 = [mlu.run_analysis_standard2_to_df(runnumber) for runnumber in runnumbers]
    analyses_standard2 = pd.concat(group_analyses_standard2).groupby(level=[0, 1]).mean()

    # # Compute the mean over all runnumbers for standard2 analysis
    # analyses_standard2_dfs = [mlu.run_analysis_standard2_to_df(runnumber) for runnumber in runnumbers]
    # analysis_standard2_mean = pd.concat(analyses_standard2_dfs).groupby(level=[0, 1]).mean()

    ## Plotting coherence
    fig, ax = plt.subplots()

    sns.heatmap(analyses_standard2[analysis_standard2_name].unstack().transpose(), ax=ax, vmin=0, vmax=1,
                cmap='inferno')

    ax.invert_yaxis()
    plu.set_heatmap_axes(ax)
    analysis_title = mlu.analysis_standard2_names[analysis_standard2_name] if not mlu.analysis_standard2_names[analysis_standard2_name] == "" else analysis_standard2_name
    ax.set_title(f'{analysis_title}')

    # Insert a textbox listing the feedback conductance
    text = ""
    # if feedback_conductance_ee != 0:
    text += f"$reg_{2}^{{exc}} \\rightarrow reg_{1}^{{inh}}={feedback_conductance_ee} mS/cm^2$\n"

    # if feedback_conductance_ei != 0:
    text += f"$reg_{2}^{{exc}} \\rightarrow reg_{1}^{{inh}}={feedback_conductance_ei} mS/cm^2$"

    if debug:
        text += f"\nruns = {runnumbers}"  # TODO comment that before  handing in

    plu.set_textbox(ax, text)

    fig.show()

    if filename_format:
        # Convert the float into a string. We are always <1, so cut off everything in front of decimal
        feedback_conductance_ee_str = "{:4.3f}".format(feedback_conductance_ee).replace(".", "_")[2:]
        feedback_conductance_ei_str = "{:4.3f}".format(feedback_conductance_ei).replace(".", "_")[2:]

        filename = filename_format.format(feedback_conductance_ee=feedback_conductance_ee_str,
                                          feedback_conductance_ei=feedback_conductance_ei_str,
                                          region=region,
                                          analysis_standard_name=analysis_standard2_name.lower())

        plu.save_figure(fig, filename, runnumbers=runnumbers,
                        feedback_conductance_ee=feedback_conductance_ee,
                        feedback_conductance_ei=feedback_conductance_ei)


def save_default():
    # filename_format = None
    analysis_standard2_name = 'coh'
    for runnumbers in runnumbers_sett:
        figure_appendix_analysis_standard_heatmap_with_feedback(runnumbers,
                                                                    analysis_standard_name=analysis_standard2_name,
                                                                    filename_format=None, debug=False)


if __name__ == "__main__":
    #save_default()

    for runnumbers in runnumbers_sett:
        for analysis_standard2_name in mlu.analysis_standard2_names.keys():
            figure_appendix_analysis_standard_heatmap_with_feedback(runnumbers,
                                                                    analysis_standard2_name=analysis_standard2_name,
                                                                    filename_format=None, debug=True)
