import matplotlib.pyplot as plt
import seaborn as sns

import matlab_utils as mlu
import settings as settings
import plot_utils as plu

runnumber = 81
l1list = [10, 19]
filename_format = 'figure_results_frequency_vs_feedforward_conductance_run{runnumber}_l1{l1}.png'


def figure_results_feedforward_conductance_frequency(runnumber, l1, filename_format):
    """
    Plots the change in region 2 frequency in dependence on the total synaptic conductance from region 1 to region 2
    :param runnumber:
    :param l1:
    :param filename_format:
    :return:
    """

    sett = mlu.get_clean_settings(runnumber)['sett']
    feedback_conductance_ei = sett['g_syn_ei_r'][0, 1]

    run_settings_loops = mlu.get_run_loops(runnumber)
    analysis_standard_reg1_df, analysis_standard_reg2_df = mlu.run_analysis_standard_to_df(runnumber)

    avgmorfreqs1 = analysis_standard_reg1_df['avgmorfreq'][l1]
    avgmorfreqs2 = analysis_standard_reg2_df['avgmorfreq'][l1]

    i_inj_exc = run_settings_loops[1]['values_excitatory'][l1].round(2)
    i_inj_inh = run_settings_loops[1]['values_inhibitory'][l1].round(2)

    synaptic_conductances = run_settings_loops[2]['values'].round(2)

    print(f"Frequency of region 1: {avgmorfreqs1[0]}")
    print(f"Starting frequency of region 2: {avgmorfreqs2[0]}")
    print(f"Ending frequency of region 2: {list(avgmorfreqs2)[-1]}")

    fig, ax = plt.subplots(figsize=(6.4, 4.4))

    sns.scatterplot(x=synaptic_conductances, y=avgmorfreqs1, s=30, ax=ax, label="Region 1")
    sns.scatterplot(x=synaptic_conductances, y=avgmorfreqs2, s=30, ax=ax, label="Region 2")

    ax.set_xlabel(r"Total synaptic conductance $g_{1 \to 2}^{e \to e, i}$ ($mS/cm^2$)")
    ax.set_ylim([39, 71])

    ax.set_ylabel('Frequency ($Hz$)')

    # ax.set_title(f"Frequency modulation through synaptic conductance")
    ax.legend(loc='upper left')

    if feedback_conductance_ei != 0:
        text = mlu.get_infobox_text(feedback_conductance_ee=None, feedback_conductance_ei=feedback_conductance_ei)
        # text = f"$reg_{2}^{{exc}} \\rightarrow reg_{1}^{{inh}}={feedback_conductance_ei} mS/cm^2$"
        plu.set_textbox(ax, text, loc='upper right')

    fig.show()

    if filename_format:
        filename = filename_format.format(runnumber=runnumber, l1=l1)
        plu.save_figure(fig, filename, runnumbers=[runnumber], l1=l1, i_inj_exc=i_inj_exc, i_inj_inh=i_inj_inh,
                        reg1_freq=avgmorfreqs1[0],
                        reg2_freq_start=avgmorfreqs2[0], reg2_freq_end=list(avgmorfreqs2)[-1])


def save_default():
    for l1 in l1list:
        figure_results_feedforward_conductance_frequency(runnumber=runnumber, l1=l1, filename_format=filename_format)
        figure_results_feedforward_conductance_frequency(runnumber=127, l1=l1, filename_format=filename_format)
        figure_results_feedforward_conductance_frequency(runnumber=106, l1=l1, filename_format=filename_format)
        figure_results_feedforward_conductance_frequency(runnumber=105, l1=l1, filename_format=filename_format)


if __name__ == "__main__":
    save_default()
