import matlab_utils as mlu

runnumber1 = 81
runnumber2 = 103

print_settings = False

if print_settings:
    print(mlu.get_clean_settings(runnumber1))
    print(mlu.get_clean_settings(runnumber2))

print(mlu.compare_settings(runnumber1, runnumber2))
