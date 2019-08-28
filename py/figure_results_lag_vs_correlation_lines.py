import os

import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np

import matlab_utils as mlu
import plot_utils as plu

filename_results_format = 'figure_results_lag_vs_correlation_lines_{analysis_info2_name}_{runnumber}.png'
filename_appendix_format = 'figure_appendix_lag_vs_correlation_lines_{analysis_info2_name}_{runnumber}.png'



def figure_results_lag_vs_correlation_lines(runnumber, signal_type, signal_from, region_from, region_to,
                                            coherence_threshold, filename_format=None):
    if region_from == region_to:
        coherence_threshold = 0

    coherences = mlu.run_analysis_standard2_to_df(runnumber)['coh']

    correlations, lags = mlu.run_analysis_info2_to_df(runnumber)
    analysis_info2_name = f'rhos_{signal_type}_{signal_from}{region_from}_reg{region_to}'

    correlations = correlations[analysis_info2_name][coherences >= coherence_threshold]

    maximum_correlations_lags = []
    min_lag = -35
    max_lag = 30  # in ms

    title = mlu.derive_analysis_info2_title(analysis_info2_name)

    fig, ax = plt.subplots(figsize=(10, 5))

    for index_condition in correlations.unstack(2).index:
        condition_correlations = correlations.loc[index_condition]
        condition_lags = lags

        sns.lineplot(x=condition_lags, y=condition_correlations, zorder=10)

        #### Filtering:
        condition_correlations[condition_lags > mlu.CORRELATION_TMAX] = 0
        condition_correlations[condition_lags < mlu.CORRELATION_TMIN] = 0


        condition_idx_of_max_correlation = condition_correlations.idxmax()
        filtered_lag = condition_lags[condition_idx_of_max_correlation]
        maximum_correlations_lags.append(filtered_lag)

    maximum_correlation_histogram, _ = np.histogram(maximum_correlations_lags, bins=lags)

    ax.axvline(mlu.CORRELATION_TMIN, linestyle='--', c='grey')
    ax.axvline(mlu.CORRELATION_TMAX, linestyle='--', c='grey')


    ax.set_xlim([mlu.CORRELATION_TMIN - 5, mlu.CORRELATION_TMAX + 5])
    ax.set_xlabel('Lag $\Delta t$ in ms')

    ax.set_ylabel('Correlation')
    ax.set_ylim([-0.1, 1])

    ax2 = ax.twinx()
    ax2.bar(x=lags[:-1], height=maximum_correlation_histogram, width=0.5, zorder=1, alpha=0.6)

    # ax2.set_yticks(np.arange(0, max(maximum_correlation_histogram)+1), 5)
    ax2.set_ylabel("Count")

    # ax.set_title(
    #     f'{title} vs Lag')

    fig.show()

    if filename_format:
        filename = filename_format.format(runnumber=runnumber, analysis_info2_name=analysis_info2_name)
        plu.save_figure(fig, filename, analysis_info2_name=analysis_info2_name, coherence_threshold=coherence_threshold)


def save_default():
    figure_results_lag_vs_correlation_lines(
        runnumber=140,
        signal_type='fper',
        signal_from='noise',
        region_from=1,
        region_to=1,
        coherence_threshold=0.95,
        filename_format=filename_results_format)
    figure_results_lag_vs_correlation_lines(
        runnumber=112,
        signal_type='fper',
        signal_from='reg',
        region_from=1,
        region_to=2,
        coherence_threshold=0.70,
        filename_format=filename_appendix_format)



if __name__ == "__main__":
    save_default()
    # figure_results_lag_vs_correlation_lines(
        # runnumber=140,
        # signal_type='fper',
        # signal_from='noise',
        # region_from=1,
        # region_to=1,
        # coherence_threshold=0.97,
        # filename_format=None)
