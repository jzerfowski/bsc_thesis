import os
import sys

# Read the category-entries from ./GridOutput/run_categories.py to be usable everywhere
sys.path.insert(0, './GridOutput/')
import run_categories

categories = run_categories.categories
excludes = run_categories.excludes

categories2 = run_categories.categories2
excludes2 = run_categories.categories2

"""Directory and filename specifications"""
output_dir = './GridOutput/'
data_dir = os.path.join(output_dir, 'Data/')
figures_dir = os.path.join(output_dir, 'Figures/')
log_dir = os.path.join(output_dir, 'log/')

## Defining output directories
reference_settings_filename = 'reference_settings.mat'
reference_settings_filepath = os.path.join(data_dir, reference_settings_filename)

template_filepath = './summary_entry.template'
run_summary_filepath = os.path.join(output_dir, 'run_summaries.txt')


tex_figures_dir = '../tex/figures/output-tmp/'

py_figures_dir = './py_figures/'
figures_save_to = './figures/'

figures_summary_file = './figures/figures_summary.txt'


def run_figures_dir(runnumber):
    return os.path.join(figures_dir, f'run{runnumber}')


## Dynamic specifications for run and settings
def run_dir(runnumber):
    return os.path.join(data_dir, f'run{runnumber}')


def run_figures_dir(runnumber):
    return os.path.join(figures_dir, f'run{runnumber}')


def run_dir(runnumber):
    return os.path.join(data_dir, f'run{runnumber}')


def run_settings_filepath(runnumber):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_settings.mat')


def run_description_filepath(runnumber):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_description.txt')


def run_description_filepath_old(runnumber):
    return os.path.join(run_dir(runnumber), f'description.txt')


def run_loop_spiketrains_filepath(runnumber, l1, l2):
    os.path.join(run_dir(runnumber), f'run{runnumber}_l1{l1}_l2{l2}.mat')


def run_analysis_standard_filepath(runnumber):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_analysis.mat')


def run_analysis_standard2_filepath(runnumber):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_analysis2.mat')


def run_analysis_info_filepath(runnumber):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_analysis_info.mat')


def run_analysis_info2_filepath(runnumber):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_analysis_info2.mat')


def run_analysis_coherencefrequency_filepath(runnumber):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_analysis_coherencefrequency.mat')


def run_spiketrain_filepath(runnumber, l1, l2):
    return os.path.join(run_dir(runnumber), f'run{runnumber}_l1{l1}_l2{l2}.mat')
