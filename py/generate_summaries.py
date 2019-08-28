#!/home/jan/anaconda3/bin/python
import os
import pprint
from string import Template
import sys

import matlab_utils as mlu
import settings as settings


def _write_run(runnumber, run_summary_fp):
    try:
        simulation_run = mlu.SimulationRun(runnumber)
        diff_reference = simulation_run.compare_to_reference(settings.reference_settings_filepath)
        result = template.substitute({'runnumber': simulation_run.runnumber, 'description': simulation_run.description,
                                      'diff_reference': pprint.pformat(diff_reference, indent=1, compact=False, width=70)})
        print(f"Writing summary for run {runnumber}")
        run_summary_fp.write(result)

    except FileNotFoundError:
        print(f"Skipping run{runnumber}. Settings file not found")


# Only get subdirectories of data_dir
run_dirs = next(os.walk(settings.data_dir))[1]

# Extract the runnumbers from the directory names
runnumbers_in_dir = ([int(run_dir[len('run'):]) for run_dir in run_dirs])

categories = settings.categories2
excludes = settings.excludes

# Get the template
with open(settings.template_filepath, 'r') as template_fp:
    template = Template(template_fp.read())

# Write the summaries
with open(settings.run_summary_filepath, 'w') as run_summary_fp:
    for category_name, details in categories.items():
        # For each category, write a header line:
        run_summary_fp.write(f"##### Category: {category_name} - {details['description']} #####")
        for runnumbers in details['runnumbers']:
            run_summary_fp.write(f"\n#### Settings: Runs {runnumbers} with the same settings except seeds ####\n")
            for runnumber in runnumbers:
                # Write each run in this category to the file:
                _write_run(runnumber, run_summary_fp)
                # If we want we can leave out those runnumber in the later run
                # excludes.add(runnumber)

    run_summary_fp.write('##### Runs Uncategorized #####\n\n')
    # We want to have the entries sorted by runnumber
    for runnumber in sorted(runnumbers_in_dir):
        if runnumber not in excludes:
            _write_run(runnumber, run_summary_fp)
