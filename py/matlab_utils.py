import warnings
import os

import scipy.io as spio
import numpy as np
import pandas as pd

import settings as settings
import pandas_utils as pdu

METHOD_CORRELATION_MAX = 'max'
METHOD_CORRELATION_LAG0 = 'lag0'
METHODS = [METHOD_CORRELATION_LAG0, METHOD_CORRELATION_MAX]

CORRELATION_TMIN = -35
CORRELATION_TMAX = 30

analysis_standard2_names = {'cohi': 'Coherence - interneurons',
                            'coh': 'Coherence - pyramidal neurons',
                            'peakcor': '?',
                            'delay': '?: Delay between areas',
                            'phasediff': 'Phase difference (pyramidal neurons)',
                            'phasediffi': 'Phase difference (interneurons)',
                            'phasediff_std': '? Phase difference (phasediff_std)',
                            'Phaselocki_12': '? (Phaselocki_12)',
                            'Phaselocke_12': '? (Phaselocke_12)'
                            }

analysis_standard_names = {
    'avgmorfreq': "Frequency", 'avgmorfreqi': "", 'CVall': "", 'CVe': "", 'CVi': "", 'delayei': "", 'freqe': "", 'freqi': "",
    'Phaselocke': "PPC value (pyramidal cells)", 'Phaselocki': "PPC value (interneurons)", 're': "", 'ri': ""
}

analysis_info2_names = {
    'rhos_fper_noise1_reg1': r"Noise_1 $\rightarrow$ Firing rate of region_1$",
    'rhos_fper_noise1_reg2': r"Noise_1 $\rightarrow$ Firing rate of region_$",
    'rhos_fper_noise2_reg1': r"Noise_2 $\rightarrow$ Firing rate of region 1",
    'rhos_fper_noise2_reg2': f"Noise_2 $\rightarrow$ Firing rate of region 2",
    'rhos_fper_reg1_reg2': "Firing rate of region 1 $\rightarrow$ region 2", 'rhos_freq_noise1_reg1': "$Noise_1$ ",
    'rhos_freq_noise1_reg2': "", 'rhos_freq_noise2_reg1': "",
    'rhos_freq_noise2_reg2': "", 'rhos_freq_reg1_reg2': "", 'rhos_power_noise1_reg1': "",
    'rhos_power_noise1_reg2': "", 'rhos_power_noise2_reg1': "", 'rhos_power_noise2_reg2': "",
    'rhos_power_reg1_reg2': "",
}


def get_infobox_text(feedback_conductance_ee, feedback_conductance_ei, runnumbers=None, debug=False, show_info_fb_inh=True, show_info_fb_exc=False):
    text = ""
    if feedback_conductance_ee and (show_info_fb_exc or feedback_conductance_ee != 0):
        # text += f"$reg_{2}^{{exc}} \\rightarrow reg_{1}^{{inh}}={feedback_conductance_ee} mS/cm^2$\n"
        text += f"$g_{{2 \\to 1}}^{{e \\to e}} = {feedback_conductance_ee} mS/cm^2$\n"

    if show_info_fb_inh or feedback_conductance_ei:
        # text += f"$reg_{2}^{{exc}} \\rightarrow reg_{1}^{{inh}}={feedback_conductance_ei} mS/cm^2$"
        text += f"$g_{{2 \\to 1}}^{{e \\to i}} = {feedback_conductance_ei} mS/cm^2$"

    if debug and runnumbers:
        text += f"\nruns = {runnumbers}"

    return text


def derive_analysis_info2_title(analysis_info2_name):
    rhos, signal_type, signal_from, region_to = analysis_info2_name.split('_')
    region_from = int(signal_from[-1])
    signal_from = signal_from[:-1]
    region_to = int(region_to[-1])
    return get_analysis_info2_title(signal_type, signal_from, region_from, region_to)


def get_analysis_info2_title(signal_type, signal_from, region_from, region_to):
    signal_title = ""
    # signal_title += "Correlation ("
    type_title = {'fper': "Firing rate", 'freq': "Frequency", 'power': "Power"}[signal_type]

    if signal_from == 'noise':
        signal_title += f"$Noise_{region_from}$"
    else:
        signal_title += f"{type_title} of region {region_from}"
    signal_title += r" $\rightarrow$ "
    signal_title += f"{type_title} of region {region_to}"

    # signal_title += ')'

    return signal_title


def get_noise_title(noiseamp, noisetype):
    noisetypes = {1: "White", 2: "Brown", 3: "Pink"}

    title = ""
    if noiseamp == 0.5:
        title += "Weak "
    elif noiseamp == 1.0:
        title += "Strong "
    else:
        title += ""

    title += noisetypes[noisetype]
    title += " noise"


class SimulationRun:
    def __init__(self, runnumber):
        self.runnumber = runnumber
        self.settings = get_settings(self.runnumber)
        self.description = get_description(self.runnumber)

    def __str__(self):
        return f'Run {runnumber} settings object'

    def compare_to_reference(self, reference_filepath):
        reference_settings = loadmat(reference_filepath)
        diff_to_reference = compare_settings_dicts(reference_settings, self.settings)
        diff_to_reference = clean_diff_to_reference(diff_to_reference)
        return diff_to_reference


def get_settings(runnumber):
    settings_matfile = loadmat(settings.run_settings_filepath(runnumber))

    return settings_matfile


def get_description(runnumber):
    description_filepath = settings.run_description_filepath(runnumber)
    description_filepath_old = settings.run_description_filepath_old(runnumber)

    if os.path.isfile(description_filepath):
        with open(description_filepath) as description_fp:
            return description_fp.read()
    elif os.path.isfile(description_filepath_old):
        with open(description_filepath_old) as description_fp:
            return description_fp.read()
    else:
        return ''


def get_spiketrains(runnumber, l1, l2):
    matfile = loadmat(settings.run_spiketrain_filepath(runnumber, l1, l2))
    return matfile['spikes_e'], matfile['spikes_i']


def get_spiketrains_df(runnumber, l1, l2):
    spikes_e, spikes_i = get_spiketrains(runnumber, l1, l2)

    spikes_excitatory = pd.DataFrame(spikes_e, columns=['neuron_idx', 't', 'region'])
    spikes_inhibitory = pd.DataFrame(spikes_i, columns=['neuron_idx', 't', 'region'])

    return spikes_excitatory, spikes_inhibitory


def clean_diff_to_reference(diff_to_reference):
    diff_fields_clean = ['fromfile', 'saveloc', 'savelocdata']

    for fieldname in diff_fields_clean:
        if fieldname in diff_to_reference['sett']:
            del diff_to_reference['sett'][fieldname]
        pass

    return diff_to_reference


def clean_settings(settings_matfile):
    sett_fields_array = ['loopIe', 'eIspecial', 'iIspecial', 'eIu', 'eIu_max', 'g_syn_loop', 'g_syn_ee_r', 'g_syn_ei_r',
                         'g_syn_ie_r', 'g_syn_ie_r']

    for fieldname in sett_fields_array:
        settings_matfile['sett'][fieldname] = np.array(settings_matfile['sett'][fieldname])

    return settings_matfile


def get_clean_settings(runnumber):
    return clean_settings(get_settings(runnumber))


def compare_dict(base, diff):
    '''
    Compares the contents of two dictionaries
    '''
    differences = {}
    base_and_diff = [x for x in base.keys() if x in diff.keys()]
    base_not_diff = list(set(base.keys()) - set(diff.keys()))
    diff_not_base = list(set(diff.keys()) - set(base.keys()))

    for name in base_and_diff:
        # check_truth = base[name] == diff[name]
        if not base[name] == diff[name]:
            differences[name] = diff[name]

    for name in diff_not_base:
        differences[name] = diff[name]

    if base_not_diff:
        differences['base_only'] = {}
        for name in base_not_diff:
            differences['base_only'][name] = base[name]
    return differences


def compare_settings(runnumber_reference, runnumber_compare):
    '''
    Expects two runnumbers and compares the settings belonging to these runnumbers.
    '''
    if not isinstance(runnumber_reference, int):
        raise Exception("From now on you should compare settings only by their runnumbers")

    settings_reference = get_settings(runnumber_reference)
    settings_compare = get_settings(runnumber_compare)

    differences = compare_settings_dicts(settings_reference, settings_compare)

    return differences


def compare_settings_dicts(settings_reference_dict, settings_compare_dict):
    differences = {}
    differences['sett'] = compare_dict(settings_reference_dict['sett'], settings_compare_dict['sett'])
    differences['para'] = compare_dict(settings_reference_dict['para'], settings_compare_dict['para'])

    return differences


def get_run_loops(runnumber):
    sett = clean_settings(get_settings(runnumber))['sett']

    loops = {}
    loopcount = 0

    ## This applies only for plotting
    for region_idx in np.where(sett['loopIe'] == 5):
        # Correction for matlab-like naming of region starting with 1
        region_idx = region_idx[0] + 1

        steps = 0
        values_excitatory = sett['eIspecial']

        values_inhibitory = sett['iIspecial']

        loopcount += 1
        loops[loopcount] = {'name': 'loopeI_special',
                            'steps': len(values_excitatory),
                            'name_readable': f'Injected current into inhibitory neurons of $reg_{region_idx}$ ($\mu A/cm^2$)',
                            'region': region_idx,
                            'values_excitatory': values_excitatory,
                            'values_inhibitory': values_inhibitory,
                            'values': values_inhibitory}

    for to_idx, from_idx in zip(*np.where(sett['g_syn_loop'] != 0)):
        if sett['g_syn_loop'][to_idx, from_idx] == 1:
            steps = int(
                np.round((sett['g_syn_r_max'] - sett['g_syn_ee_r'][to_idx, from_idx]) / sett['g_syn_r_step'] + 1))
            values = np.linspace(sett['g_syn_ee_r'][to_idx, from_idx], sett['g_syn_r_max'], steps)

            loopcount += 1
            loops[loopcount] = {'name': 'g_syn_loop',
                                'region_from': from_idx,
                                'region_to': to_idx,
                                'steps': int(np.round(
                                    (sett['g_syn_r_max'] - sett['g_syn_ee_r'][to_idx, from_idx]) / sett[
                                        'g_syn_r_step'] + 1)),
                                'name_readable': fr"Total synaptic conductance $reg_{from_idx+1} \rightarrow reg_{to_idx+1}$ ($mS/cm^2$)",
                                'values': values}
        else:
            raise NotImplementedError('No other values than 1 implemented yet')

    return loops


def run_analysis_standard_to_df(runnumber):
    analysis_standard_mat = loadmat(settings.run_analysis_standard_filepath(runnumber))

    analysis_standard_df_reg1 = pd.DataFrame()
    analysis_standard_df_reg2 = pd.DataFrame()

    for key in analysis_standard_names.keys():
        analysis_standard_df_reg1[key] = pd.DataFrame(analysis_standard_mat[key][:, :, 0]).stack()
        analysis_standard_df_reg2[key] = pd.DataFrame(analysis_standard_mat[key][:, :, 1]).stack()

    analysis_standard_df_reg1.index.names = ['loop1', 'loop2']
    analysis_standard_df_reg2.index.names = ['loop1', 'loop2']

    return analysis_standard_df_reg1, analysis_standard_df_reg2


def run_analysis_standard2_to_df(runnumber):
    analysis2_mat = loadmat(settings.run_analysis_standard2_filepath(runnumber))

    analysis2_df = pd.DataFrame()

    for key in analysis_standard2_names.keys():
        analysis2_df[key] = pd.DataFrame(analysis2_mat[key]).stack()
    analysis2_df.index.names = ['l1', 'l2']

    return analysis2_df


def run_analysis_info2_to_df(runnumber):
    analysis_coherences_mat = loadmat(settings.run_analysis_info2_filepath(runnumber))

    index_names = ['l1', 'l2', 'lag']

    analysis_info2_df = pd.DataFrame()
    analysis_info2_lags = analysis_coherences_mat['rhos_lags']

    for analysis_name in analysis_info2_names.keys():
        if analysis_name not in analysis_coherences_mat.keys():
            warnings.warn(f"{analysis_name} missing in {settings.run_analysis_info2_filepath(runnumber)}")
            continue
        analysis_info2_df[analysis_name] = pdu.series_from_ndim_array(analysis_coherences_mat[analysis_name],
                                                                      index_names=index_names)

    return analysis_info2_df, analysis_info2_lags


def get_run_correlations_single(runnumber, analysis_info2_name, method):
    warnings.warn(f"Deprecated. Rather use {get_run_correlations}.")

    return get_run_correlations(runnumber, method)[analysis_info2_name]


def get_run_correlations_single_and_lag(runnumber, method, analysis_info2_name):
    correlations_df = get_run_correlations(runnumber, method, analysis_info2_names=[analysis_info2_name])
    return correlations_df[analysis_info2_name], correlations_df[f'{analysis_info2_name}_lag']


def get_run_correlations(runnumber, method, analysis_info2_names=None):
    assert (method in METHODS)

    analysis_info2_df, analysis_info2_lags = run_analysis_info2_to_df(runnumber)
    correlations = pd.DataFrame()

    t_min = -50
    t_max = 0

    if analysis_info2_names is None:
        analysis_info2_names = analysis_info2_df.columns

    for analysis_info2_name in analysis_info2_names:
        if method == METHOD_CORRELATION_MAX:
            correlations[analysis_info2_name] = analysis_info2_df[analysis_info2_name].max(level=[0, 1])
            correlations[f'{analysis_info2_name}_lag_idx'] = [max_idx[2] for max_idx in
                                                              analysis_info2_df[analysis_info2_name].groupby(
                                                                  level=[0, 1]).idxmax()]
            correlations[f'{analysis_info2_name}_lag'] = analysis_info2_lags[
                correlations[f'{analysis_info2_name}_lag_idx']]
        elif method == METHOD_CORRELATION_LAG0:
            lag0_index = np.abs(analysis_info2_lags).argmin()
            correlations[analysis_info2_name] = analysis_info2_df[analysis_info2_name].loc[:, :, lag0_index]
            correlations[f'{analysis_info2_name}_lag'] = 0
    return correlations


def get_max_correlations(runnumber, t_min=CORRELATION_TMIN, t_max=CORRELATION_TMAX):
    analysis_info2_df, analysis_info2_lags = run_analysis_info2_to_df(runnumber)

    idx_min = np.argwhere(analysis_info2_lags == t_min)[0, 0]
    idx_max = np.argwhere(analysis_info2_lags == t_max)[0, 0]

    correlations_max = analysis_info2_df.loc[(slice(None), slice(None), slice(idx_min, idx_max)), :].max(level=[0, 1])

    return correlations_max


def loadmat(filename):
    '''
    https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''

    def _check_keys(d):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in d:
            if isinstance(d[key], spio.matlab.mio5_params.mat_struct):
                d[key] = _todict(d[key])
        return d

    def _todict(matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, spio.matlab.mio5_params.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        '''
        A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        '''
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem, spio.matlab.mio5_params.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif isinstance(sub_elem, np.ndarray):
                elem_list.append(_tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list

    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)
