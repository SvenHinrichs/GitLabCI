import os

# Whitelist files
ch_file = f'bin{os.sep}03_WhiteLists{os.sep}changedmodels.txt'
wh_file = f'bin{os.sep}03_WhiteLists{os.sep}IBPSA_whitelist_model.txt'
exit_file = f'bin{os.sep}06_Configfiles{os.sep}exit.sh'
new_ref_file = f'bin{os.sep}03_WhiteLists{os.sep}new_ref.txt' 
ref_file = f'bin{os.sep}03_WhiteLists{os.sep}ref_list.txt'


# Ci Templates
reg_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}regression_test.txt'
write_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}check_model.txt'
sim_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}simulate_model.txt'
page_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}deploy{os.sep}gitlab_pages.txt'
ibpsa_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}deploy{os.sep}IBPSA_Merge.txt'
main_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}gitlab-ci.txt'

temp_dir = f'bin{os.sep}07_templates{os.sep}03_ci_templates'

# Charts
chart_temp = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}google_chart.txt'
index_temp = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}index.txt'
layout_temp = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}layout_index.txt'

index_path = f'bin{os.sep}07_templates{os.sep}02_charts'
chart_dir = f'bin{os.sep}07_templates{os.sep}02_charts'

# Reference files
ref_file_path = f'Resources{os.sep}ReferenceResults{os.sep}Dymola'
resource_dir = f'Resources{os.sep}Scripts{os.sep}Dymola'





