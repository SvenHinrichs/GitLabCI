import os

# Whitelist files
ch_file = f'bin{os.sep}03_WhiteLists{os.sep}changedmodels.txt'
wh_file = f'bin{os.sep}03_WhiteLists{os.sep}IBPSA_whitelist_model.txt'
exit_file = f'bin{os.sep}06_Configfiles{os.sep}exit.sh'
new_ref_file = f'bin{os.sep}03_WhiteLists{os.sep}new_ref.txt' 
ref_file = f'bin{os.sep}03_WhiteLists{os.sep}ref_list.txt'
ref_whitelist = f'..{os.sep}bin{os.sep}03_WhiteLists{os.sep}ref_Whitelist.txt'


# Ci Templates
reg_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}regression_test.txt'
write_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}check_model.txt'
sim_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}simulate_model.txt'
page_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}deploy{os.sep}gitlab_pages.txt'
ibpsa_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}deploy{os.sep}IBPSA_Merge.txt'
main_temp = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}gitlab-ci.txt'
main_yml = f'.gitlab-ci.yml'

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

# image_name
image_name = 'registry.git.rwth-aachen.de/ebc/ebc_intern/dymola-docker:miniconda-latest'
project_name = 'SvenHinrichs/GitLabCI'
variable_main_list = ['Praefix_Branch: "Correct_HTML_"', 'TARGET_BRANCH: $CI_COMMIT_REF_NAME', 'Newbranch: ${Praefix_Branch}${CI_COMMIT_REF_NAME}', 'Github_Repository: SvenHinrichs/GitLabCI', 'GITLAB_Page: "https://svenhinrichs.pages.rwth-aachen.de/GitLabCI"']

# Pull Request Comment
#self.post_comment_message = f'Error in regression test.\\n Compare the results on the following page {self.page_url}'
